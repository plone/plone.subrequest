Overview
========

plone.subrequest provides a mechanism for issuing subrequests under Zope2.

Usage
=====

    >>> from plone.subrequest import subrequest
    >>> response = subrequest('foo/bar')
    >>> data = response.body or response.stdout.getvalue()
