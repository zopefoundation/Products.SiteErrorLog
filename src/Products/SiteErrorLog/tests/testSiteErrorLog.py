##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import logging
import sys
import unittest

import Testing.testbrowser
import Testing.ZopeTestCase
import transaction
import Zope2
import Zope2.App
from OFS.Folder import Folder
from OFS.Folder import manage_addFolder
from Testing.makerequest import makerequest
from zope.component import adapter
from zope.component import provideHandler
from zope.component.globalregistry import globalSiteManager
from zope.event import notify
from ZPublisher.pubevents import PubFailure
from ZPublisher.WSGIPublisher import publish
from ZPublisher.WSGIPublisher import transaction_pubevents

from ..interfaces import IErrorRaisedEvent
from ..SiteErrorLog import IPubFailureSubscriber
from ..SiteErrorLog import manage_addErrorLog


class SiteErrorLogTests(unittest.TestCase):

    def setUp(self):
        Zope2.startup_wsgi()
        transaction.begin()
        self.app = makerequest(Zope2.app())
        try:
            if not hasattr(self.app, 'error_log'):
                # If ZopeLite was imported, we have no default error_log
                from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
                self.app._setObject('error_log', SiteErrorLog())
            self.app.manage_addDTMLMethod('doc', '')

            self.logger = logging.getLogger('Zope.SiteErrorLog')
            self.log = logging.handlers.BufferingHandler(sys.maxsize)
            self.logger.addHandler(self.log)
            self.old_level = self.logger.level
            self.logger.setLevel(logging.ERROR)
        except Exception:
            self.tearDown()

    def tearDown(self):
        self.logger.removeHandler(self.log)
        self.logger.setLevel(self.old_level)
        transaction.abort()
        self.app._p_jar.close()

    def testInstantiation(self):
        # Retrieve the error_log by ID
        sel_ob = getattr(self.app, 'error_log', None)

        # Does the error log exist?
        self.assertIsNotNone(sel_ob)

        # Is the __error_log__ hook in place?
        self.assertEqual(self.app.__error_log__, sel_ob)

    def testSimpleException(self):
        # Grab the Site Error Log and make sure it's empty
        sel_ob = self.app.error_log
        previous_log_length = len(sel_ob.getLogEntries())

        # Fill the DTML method at self.root.doc with bogus code
        dmeth = self.app.doc
        dmeth.manage_upload(file="""<dtml-var expr="1/0">""")

        # Faking the behavior of the WSGIPublisher (object acquisition,
        # view calling and failure notification on exception).
        try:
            dmeth.__call__()
        except ZeroDivisionError:
            self.app.REQUEST['PUBLISHED'] = dmeth
            notify(PubFailure(self.app.REQUEST, sys.exc_info(), False))

        # Now look at the SiteErrorLog, it has one more log entry
        self.assertEqual(len(sel_ob.getLogEntries()), previous_log_length + 1)

    def testEventSubscription(self):
        # Fill the DTML method at self.root.doc with bogus code
        dmeth = self.app.doc
        dmeth.manage_upload(file="""<dtml-var expr="1/0">""")

        event_logs = []

        @adapter(IErrorRaisedEvent)
        def notifyError(evt):
            event_logs.append(evt)

        provideHandler(notifyError)
        # Faking the behavior of the WSGIPublisher (object acquisition,
        # view calling and failure notification on exception).
        try:
            dmeth.__call__()
        except ZeroDivisionError:
            self.app.REQUEST['PUBLISHED'] = dmeth
            notify(PubFailure(self.app.REQUEST, sys.exc_info(), False))

        self.assertEqual(len(event_logs), 1)
        self.assertEqual(event_logs[0]['type'], 'ZeroDivisionError')
        self.assertEqual(event_logs[0]['username'], 'Anonymous User')

    def testConflictErrorRetry(self):
        # If a transient error is encountered and the request can be
        # retried, don't hand it to the error log.
        from ZODB.POSException import ConflictError

        def raise_conflict():
            raise ConflictError('Oops')

        dmeth = self.app.doc
        dmeth.raise_conflict = raise_conflict
        event_logs = []
        self.app.REQUEST.set('PATH_INFO', '/doc')
        self.app.REQUEST.retry_max_count = 1  # Allow a single retry
        self.logger.setLevel(logging.INFO)

        @adapter(IErrorRaisedEvent)
        def notifyError(evt):
            event_logs.append(evt)

        provideHandler(notifyError)
        # Faking the behavior of the WSGIPublisher (object acquisition,
        # view calling and failure notification on exception).
        try:
            dmeth.raise_conflict()
        except ConflictError:
            self.app.REQUEST['PUBLISHED'] = dmeth
            notify(PubFailure(self.app.REQUEST, sys.exc_info(), False))

        self.assertEqual(len(event_logs), 0)
        self.assertEqual(len(self.log.buffer), 1)
        self.assertEqual(self.log.buffer[0].levelname, 'INFO')
        self.assertEqual(
            self.log.buffer[0].getMessage(),
            'ConflictError at /doc: Oops. Request will be retried.')

        # Second try should fail.
        self.app.REQUEST.retry_max_count = 0
        try:
            dmeth.raise_conflict()
        except ConflictError:
            self.app.REQUEST['PUBLISHED'] = dmeth
            notify(PubFailure(self.app.REQUEST, sys.exc_info(), False))

        self.assertEqual(len(event_logs), 1)
        self.assertEqual(event_logs[0]['type'], 'ConflictError')
        self.assertEqual(event_logs[0]['username'], 'Anonymous User')

    def testForgetException(self):
        elog = self.app.error_log

        # Create a predictable error
        try:
            raise AttributeError('DummyAttribute')
        except AttributeError:
            self.app.REQUEST['PUBLISHED'] = elog
            notify(PubFailure(self.app.REQUEST, sys.exc_info(), False))

        previous_log_length = len(elog.getLogEntries())

        entries = elog.getLogEntries()
        self.assertEqual(entries[0]['value'], 'DummyAttribute')

        # Kick it
        elog.forgetEntry(entries[0]['id'])

        # Really gone?
        self.assertEqual(len(elog.getLogEntries()), previous_log_length - 1)

    def testIgnoredException(self):
        # Grab the Site Error Log
        sel_ob = self.app.error_log
        previous_log_length = len(sel_ob.getLogEntries())

        # Tell the SiteErrorLog to ignore ZeroDivisionErrors
        current_props = sel_ob.getProperties()
        ignored = list(current_props['ignored_exceptions'])
        ignored.append('ZeroDivisionError')
        sel_ob.setProperties(current_props['keep_entries'],
                             copy_to_zlog=current_props['copy_to_zlog'],
                             ignored_exceptions=ignored)

        # Fill the DTML method at self.root.doc with bogus code
        dmeth = self.app.doc
        dmeth.manage_upload(file="""<dtml-var expr="1/0">""")

        # Faking the behavior of the WSGIPublisher (object acquisition,
        # view calling and failure notification on exception).
        try:
            dmeth.__call__()
        except ZeroDivisionError:
            self.app.REQUEST['PUBLISHED'] = dmeth
            notify(PubFailure(self.app.REQUEST, sys.exc_info(), False))

        # Now look at the SiteErrorLog, it must have the same number of
        # log entries
        self.assertEqual(len(sel_ob.getLogEntries()), previous_log_length)

    def testEntryID(self):
        elog = self.app.error_log

        # Create a predictable error
        try:
            raise AttributeError('DummyAttribute')
        except AttributeError:
            self.app.REQUEST['PUBLISHED'] = elog
            notify(PubFailure(self.app.REQUEST, sys.exc_info(), False))

        entries = elog.getLogEntries()
        entry_id = entries[0]['id']

        self.assertIn(
            entry_id,
            self.log.buffer[-1].msg,
            (entry_id, self.log.buffer[-1].msg)
        )

    def testCleanup(self):
        # Need to make sure that the __error_log__ hook gets cleaned up
        self.app._delObject('error_log')
        self.assertEqual(getattr(self.app, '__error_log__', None), None)


class SiteErrorLogUITests(Testing.ZopeTestCase.FunctionalTestCase):

    def setUp(self):
        super().setUp()

        Zope2.App.zcml.load_site(force=True)

        uf = self.app.acl_users
        uf.userFolderAddUser('manager', 'manager_pass', ['Manager'], [])

        # Why is this neccessary, shouldn't the test get a new app every time?
        if not hasattr(self.app, 'error_log'):
            manage_addErrorLog(self.app)
        self.error_log = self.app.error_log

        self.browser = Testing.testbrowser.Browser()
        self.browser.login('manager', 'manager_pass')
        self.browser.open('http://localhost/error_log/manage_main')

    def testSubmitRetainsIgnoredExceptionsUnchanged(self):
        # Checks the fix for
        # https://github.com/zopefoundation/Products.SiteErrorLog/issues/13
        ignoredExceptions = self.browser.getControl(
            label='Ignored exception types')
        self.assertEqual(
            ignoredExceptions.value,
            'Unauthorized\nNotFound\nRedirect')  # default value
        ignoredExceptions.value = 'Unauthorized\nFnord'
        self.assertNotIn('Changed properties', self.browser.contents)
        self.browser.getControl('Save Changes').click()
        self.assertIn('Changed properties', self.browser.contents)
        ignoredExceptions = self.browser.getControl(
            label='Ignored exception types')
        self.assertEqual(ignoredExceptions.value, 'Unauthorized\nFnord')


class WsgiErrorlogIntegrationLayer(Testing.ZopeTestCase.layer.ZopeLite):
    """The tests using this layer commit transactions. Therefore,
    we avoid persistent changes there and build the complete
    support structure in this layer.
    """
    @classmethod
    def setUp(cls):
        # Apparently, other tests have already registered the
        #   handler below, even twice
        #   Clean up those registrations and
        #   make a single clean registration
        #   remember when we must remove our registration
        regs = [r for r in globalSiteManager.registeredHandlers()
                if r.factory is IPubFailureSubscriber
                ]
        if regs:
            globalSiteManager.unregisterHandler(IPubFailureSubscriber)
        cls._unregister = not regs
        globalSiteManager.registerHandler(IPubFailureSubscriber)
        # Set up our test structure
        #   /
        #     sel_f1/
        #             error_log
        #             sel_f2/
        #                    error_log
        app = Testing.ZopeTestCase.app()
        # first level folder
        manage_addFolder(app, 'sel_f1')
        sel_f1 = app.sel_f1
        # second level folder
        manage_addFolder(sel_f1, 'sel_f2')
        sel_f2 = sel_f1.sel_f2
        # put an error log in each of those folders
        # (used in `test_correct_log_*`)
        for f in (sel_f1, sel_f2):
            manage_addErrorLog(f)
            el = f.error_log
            el._ignored_exceptions = ()  # do not ignore exceptions
        transaction.commit()
        # make `manage_delObjects` temporarily public
        cls._saved_roles = Folder.manage_delObjects__roles__
        Folder.manage_delObjects__roles__ = None  # public

    @classmethod
    def tearDown(cls):
        Folder.manage_delObjects__roles__ = cls._saved_roles
        if cls._unregister:
            globalSiteManager.unregisterHandler(IPubFailureSubscriber)
        app = Testing.ZopeTestCase.app()
        app._delOb('sel_f1')
        transaction.commit()


class WsgiErrorlogIntegrationTests(Testing.ZopeTestCase.ZopeTestCase):
    layer = WsgiErrorlogIntegrationLayer

    # we override `ZopeTestCase.setUp` by purpose
    def setUp(self):
        app = self.app = Testing.ZopeTestCase.app()
        self.f1 = app.sel_f1
        self.f2 = self.f1.sel_f2
        self.el1 = self.f1.error_log
        self.el2 = self.f2.error_log

    # overridden by purpose
    def tearDown(self):
        self._clear_els()

    def _clear_els(self):
        for el in (self.el1, self.el2):
            el._getLog()[:] = []

    def _get_el_nos(self):
        return tuple(len(el._getLog()) for el in (self.el1, self.el2))

    def test_correct_log_traversal_2(self):
        self._request('sel_f1/sel_f2/missing')
        self.assertEqual(self._get_el_nos(), (0, 1))

    def test_correct_log_traversal_1(self):
        self._request('sel_f1/missing')
        self.assertEqual(self._get_el_nos(), (1, 0))

    def test_correct_log_method_2(self):
        self._request('sel_f1/sel_f2/manage_delObjects', dict(id='missing'))
        self.assertEqual(self._get_el_nos(), (0, 1))

    def test_correct_log_method_1(self):
        self._request('sel_f1/manage_delObjects', dict(id='missing'))
        self.assertEqual(self._get_el_nos(), (1, 0))

    def _request(self, url, params=None):
        app = self.app
        request = app.REQUEST
        request.environ['PATH_INFO'] = url
        if params:
            request.form.update(params)
            request.other.update(params)
        try:
            with transaction_pubevents(request, request.response):
                publish(request, (app, 'Zope', False))
        except Exception:
            pass
