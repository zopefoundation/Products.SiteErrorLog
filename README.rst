.. image:: https://github.com/zopefoundation/Products.SiteErrorLog/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/zopefoundation/Products.SiteErrorLog/actions/workflows/tests.yml

.. image:: https://coveralls.io/repos/github/zopefoundation/Products.SiteErrorLog/badge.svg?branch=master
   :target: https://coveralls.io/github/zopefoundation/Products.SiteErrorLog?branch=master

.. image:: https://img.shields.io/pypi/v/Products.SiteErrorLog.svg
   :target: https://pypi.org/project/Products.SiteErrorLog/
   :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/Products.SiteErrorLog.svg
   :target: https://pypi.org/project/Products.SiteErrorLog/
   :alt: Supported Python versions


Products.SiteErrorLog
=====================

The SiteErrorLog object is a valuable debugging aid. It records all exceptions
happening in its container and all subfolders as your site's code executes.

SiteErrorLog recorded errors are not persistent, they are stored in RAM and
thus disappear when the Zope process restarts.
