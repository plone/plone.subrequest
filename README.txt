Overview
========

plone.subrequest provides a mechanism for issuing subrequests under Zope2.

Installation
============

Plone 4
-------

An entry point is provided so no special installation is required past adding
`plone.subrequest` to your instance's `eggs`.

Zope 2.12 without Plone
-----------------------

Load this package's ZCML in the usual manner.

Zope 2.10
---------

You must install ZPublisherEventsBackport_ to use this package with Zope 2.10
and load both package's ZCML. The tests require Zope 2.12 / Python 2.6 so will
not run.

.. _ZPublisherEventsBackport: http://pypi.python.org/pypi/ZPublisherEventsBackport

Usage
=====

Basic usage
-----------

.. test-case: absolute

Call ``subrequest(url)``, it returns a response object.

    >>> from plone.subrequest import subrequest
    >>> response = subrequest('/folder1/@@url')

The output of the response is normally written to the response body.

    >>> response.body
    'http://nohost/folder1'

.. test-case: response-write

Be aware that some code may call ``response.write(data)``

    >>> response = subrequest('/@@response-write')
    >>> response.stdout.getvalue()
    'Some data.\nSome more data.\n'

so it's usually best to retrieve the output with:

    >>> result = response.body or response.stdout.getvalue()

Relative paths
--------------

.. test-case: relative

Relative paths are resolved relative to the parent request's location:

    >>> request = traverse('/folder1/@@test')
    >>> response = subrequest('folder1A/@@url')
    >>> response.body
    'http://nohost/folder1/folder1A'

.. test-case: relative-default-view

This takes account of default view's url.

    >>> request = traverse('/folder1')
    >>> request['URL']
    'http://nohost/folder1/@@test'
    >>> response = subrequest('folder1A/@@url')
    >>> response.body
    'http://nohost/folder1/folder1A'

Virtual hosting
---------------

.. test-case: virtual-hosting

When virtual hosting is used, absolute paths are traversed from the virtual host root.

    >>> request = traverse('/VirtualHostBase/http/example.org:80/folder1/VirtualHostRoot/')
    >>> response = subrequest('/folder1A/@@url')
    >>> response.body
    'http://example.org/folder1A'

Specifying the root
-------------------

.. test-case: specify-root

You may also set the root object explicitly

    >>> app = layer['app']
    >>> response = subrequest('/folder1A/@@url', root=app.folder1)
    >>> response.body
    'http://nohost/folder1/folder1A'

Error responses
---------------

.. test-case: not-found

Subrequests may not be found.

    >>> response = subrequest('/not-found')
    >>> response.status
    404

.. test-case: error-response

Or might raise an error.

    >>> response = subrequest('/@@error')
    >>> response.status
    500

.. test-case: status-ok

So check for the expected status.

    >>> response = subrequest('/')
    >>> response.status
    200
