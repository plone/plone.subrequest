Changelog
=========

1.7.1 (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- Provide an exception-handler for rewriting Unauthorized to 401's.
  [jensens]

Bug fixes:

- *add item here*


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
