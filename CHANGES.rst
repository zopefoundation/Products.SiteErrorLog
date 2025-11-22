Changelog
=========

7.1 (unreleased)
----------------


7.0 (2025-11-20)
----------------

- Switch to PEP 420 native namespace.

- Add support for Python 3.12, 3.13 and 3.14.

- Drop support for Python 3.7, 3.8 and 3.9.


6.0 (2023-02-01)
----------------

- Drop support for Python 2.7, 3.5, 3.6.


5.7 (2022-12-16)
----------------

- Fix insidious buildout configuration bug for tests against Zope 4.

- Add support for Python 3.11.


5.6 (2022-07-05)
----------------

- Add support for Python 3.10.

- Render date in addition to time in ZMI error log.
  (`#31 <https://github.com/zopefoundation/Products.SiteErrorLog/pull/31>`_)


5.5 (2021-03-15)
----------------

- Add support for Python 3.9.

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
