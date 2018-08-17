Changelog
=========

5.0 (unreleased)
----------------

- Drop support for Zope 2, require Zope >= 4.0b6 now.

- Add support for Python 3.5 and 3.6.

- Drop `ZServer` dependency.

- Add ``IPubFailure`` event handler so it writes error log entries again.

- Bring back Application initialization (creation of `SiteErrorLog` in the
  ZODB on first startup).


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
