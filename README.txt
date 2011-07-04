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
