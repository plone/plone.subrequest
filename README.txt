Overview
========

plone.subrequest provides a mechanism for issuing subrequests under Zope2.

Installation
============

Plone 4
-------

An entry point is provided so no special installation is required.

Zope 2.12 without Plone
-----------------------

Load this package's ZCML in the usual manner.

Zope 2.10
---------

You must install ZPublisherEventsBackport_ to use this package with Zope 2.10
and load both package's ZCML. The require Zope 2.12 / Python 2.6 so will not
run.

.. _ZPublisherEventsBackport: http://pypi.python.org/pypi/ZPublisherEventsBackport

Usage
=====

A subrequest returns a response object.

    >>> from plone.subrequest import subrequest
    >>> response = subrequest('/folder1/@@url')

The output of the response is normally written to the response body.

    >>> response.body
    'http://nohost/folder1'

.. test-case: response-write

But some code calls ``response.write(data)``

    >>> response = subrequest('/@@write')
    >>> response.stdout.getvalue()
    'Some data.\nSome more data.\n'

so it's usually best to retrieve the output with:

    >>> result = response.body or response.stdout.getvalue()

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

So check that the ``response.status == 200``.

    >>> response = subrequest('/')
    >>> response.status
    200
