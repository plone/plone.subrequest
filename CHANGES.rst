Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

2.0.0b1 (2022-09-07)
--------------------

Breaking changes:


- Drop Python 2 support and update code style.
  [jensens] (#25)


1.9.3 (2020-09-26)
------------------

Bug fixes:


- Fixed deprecation warning for zope.site.hooks.
  [maurits] (#24)


1.9.2 (2020-04-22)
------------------

Bug fixes:


- Minor packaging updates. (#1)


1.9.1 (2019-04-29)
------------------

Bug fixes:


- fix regression bug which was breaking in Python 2.7 when tiles contain non-ascii characters [MrTango] (#22)


1.9.0 (2018-12-11)
------------------

Breaking changes:

- Remove five.globalrequest dependency.
  It has been deprecated upstream (on Zope 4).
  [gforcada]


1.8.6 (2018-09-23)
------------------

New features:

- Fix importsi without ZServer
  [pbauer]

Bug fixes:

- More Python 3 compatibility.
  [ale-rt, thet]

- Make test dependency on Archetypes optional.
  [davisagli]


1.8.5 (2018-01-30)
------------------

Bug fixes:

- Add Python 2 / 3 compatibility
  [pbauer]


1.8.4 (2017-09-06)
------------------

New features:

- Add support for Zope exception views when explicit exception handler
  is not defined
  [datakurre]

Bug fixes:

- Fix issue where the example unauthorized_exception_handler did
  not properly set response status code
  [datakurre]


1.8.3 (2017-08-30)
------------------

Bug fixes:

- Reverted "Remove vurl-parts from path", which resulted in broken p.a.mosaic pages
  [thet]


1.8.2 (2017-07-20)
------------------

Bug fixes:

- Remove vurl-parts from path
  [awello]


1.8.1 (2017-06-28)
------------------

Bug fixes:

- Remove unittest2 dependency
  [kakshay21]


1.8 (2016-11-01)
----------------

New features:

- Provide an exception-handler for rewriting Unauthorized to 401's.
  [jensens]


1.7.0 (2016-05-04)
------------------

New:

- Allow to pass a custom exception handler for the response.
  [jensens]

Fixes:

- When a subrequest modified the DB (or prior to the subrequest the main request),
  the oids annotated to the requests were doubled with each subsequent subrequest.
  This resulted in out-of-memory errors when using lots of subrequests,
  such as it happens on Mosaic based sites with a certain amount of tiles.
  Fixed by only adding new oids, not already known by parent request.
  [jensens]

- Housekeeping: isort imports, autopep8, minor manual cleanup (no zope.app. imports).
  [jensens]


1.6.11 (2015-09-07)
-------------------

- propagate IDisableCSRFProtection interface on subrequest to parent request object
  [vangheem]


1.6.10 (2015-08-14)
-------------------

- propagate registered safe writes from plone.protect to parent request object.
  [vangheem]


1.6.9 (2015-03-21)
------------------

- Workaround for broken test because of missing dependency declaration in
  upstream package, see https://github.com/plone/plone.app.blob/issues/19
  for details.
  [jensens]

- Housekeeping and code cleanup (pep8, et al).
  [jensens]

- Fix issue where new cookies from the main request.response are not passed to
  subrequests.
  [datakurre]

- normalise request path_info so that string indexing works properly.
  [gweiss]


1.6.8 (2014-03-04)
------------------
- Handle sub-requests which contain a doubled // in the path.
  [gweis]

1.6.7 (2012-10-22)
------------------

- Ensure correct handling of bare virtual hosting urls.
  [elro]

1.6.6 (2012-06-29)
------------------

- Log errors that occur handling a subrequest to help debug plone.app.theming
  errors including content from a different url
  [anthonygerrard]

1.6.5 (2012-04-15)
------------------

- Ensure parent url is a string and not unicode.
  [davisagli]

1.6.4 - 2012-03-22
------------------

- Fix problems with double encoding some unicode charse by not copying too
  many ``other`` variables.
  [elro]

1.6.3 - 2012-02-12
------------------

- Copy ``other`` request variables such as ``LANGUAGE`` to subrequest.
  [elro]

1.6.2 - 2011-07-04
------------------

- Handle spaces in default documents. http://dev.plone.org/plone/ticket/12278

1.6.1 - 2011-07-04
------------------

- Move tests to package directory to making testing possible when installed
  normally.

1.6 - 2011-06-06
----------------

- Ensure url is a string and not unicode.
  [elro]

1.6b2 - 2011-05-20
------------------

- Set PARENT_REQUEST and add ISubRequest interface to subrequests.
  [elro]

1.6b1 - 2011-02-11
------------------

- Handle IStreamIterator.
  [elro]

- Simplify API so ``response.getBody()`` always works.
  [elro]

1.5 - 2010-11-26
----------------

- Merge cookies from subrequest response into parent response.
  [awello]

1.4 - 2010-11-10
----------------

- First processInput, then traverse (fixes #11254)
  [awello]

1.3 - 2010-08-24
----------------

- Fixed bug with virtual hosting and quoted paths.
  [elro]

1.2 - 2010-08-16
----------------

- Restore zope.component site after subrequest.
  [elro]

1.1 - 2010-08-14
----------------

- Virtual hosting, relative url and error response support.
  [elro]

1.0 - 2010-07-28
----------------

- Initial release.
  [elro]
