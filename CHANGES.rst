Changelog
=========

5.5 (unreleased)
----------------

- Add support for Python 3.9

- Update configuration for version 5 of ``isort``


5.4 (2020-02-06)
----------------

- Log transient errors that can be re-tried as INFO only
  (`#21 <https://github.com/zopefoundation/Products.SiteErrorLog/issues/21>`_)


5.3 (2019-04-13)
----------------

- stricter flake8 configuration

- add badges and additional information links to package information

- Make sure Zope 4 ZMI shows no add dialog
  (`#19 <https://github.com/zopefoundation/Products.SiteErrorLog/issues/19>`_)


5.2 (2019-03-19)
----------------

- Ability to report problems caused by method calls (such as
  ``manage_delObjects``).

- Ability to report traversal problems.
  (`#17 <https://github.com/zopefoundation/Products.SiteErrorLog/issues/17>`_)

- Specify supported Python versions using ``python_requires`` in setup.py.
  (`Zope#481 <https://github.com/zopefoundation/Zope/issues/481>`_)

- Add support for Python 3.8.


5.1 (2018-12-18)
----------------

- Flake8 the code.

- Ignored exception types no longer accidentally get converted to bytes and back
  on Python 3.
  (`#13 <https://github.com/zopefoundation/Products.SiteErrorLog/issues/13>`_)

5.0 (2018-11-06)
----------------

- Drop support for Zope 2, require Zope >= 4.0b6 now.

- Add support for Python 3.5, 3.6 and 3.7.

- Drop `ZServer` dependency.

- Add ``IPubFailure`` event handler so it writes error log entries again.

- Bring back Application initialization (creation of `SiteErrorLog` in the
  ZODB on first startup).

- Style forms for Bootstrap ZMI.
  (`#12 <https://github.com/zopefoundation/Products.SiteErrorLog/pull/12>`_)


4.0 (2016-07-22)
----------------

- Add configure.zcml with deprecatedManageAddDelete directive.

3.0 (2016-07-19)
----------------

- Drop `test` and `zope212` setuptools extras.

- Add error event.

2.13.2 (2014-02-10)
-------------------

- Release as a separate package (previously in Zope2).
