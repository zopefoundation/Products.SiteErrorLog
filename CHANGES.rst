Changelog
=========

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
