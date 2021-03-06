Usage
=====

Basic usage
-----------

.. test-case: absolute

Call ``subrequest(url)``, it returns a response object.

    >>> from plone.subrequest import subrequest
    >>> response = subrequest('/folder1/@@url')
    >>> response.getBody()
    b'http://nohost/folder1'

.. test-case: response-write

``response.getBody()`` also works for code that calls ``response.write(data)``.
This one returns a text/non-byte value.

    >>> response = subrequest('/@@response-write')
    >>> response.getBody()
    'Some data.\nSome more data.\n'

But in this case ``response.getBody()`` may only be called once.

    >>> response.getBody()
    Traceback (most recent call last):
        ...
    ValueError: I/O operation on closed file

Accessing the response body as a file
-------------------------------------

.. test-case: stdout

Some code may call ``response.write(data)``.

    >>> response = subrequest('/@@response-write')

In which case you may access response.stdout as file.

    >>> response.stdout.seek(0, 0) or 0  # Py2 returns None, Py3 returns new position
    0
    >>> list(response.stdout)
    ['Some data.\n', 'Some more data.\n']

You can test whether a file was returned using ``response._wrote``.

    >>> response._wrote
    1

When you're done, close the file:

    >>> response.stdout.close()

.. test-case: response-outputBody

Use ``response.outputBody()`` to ensure the body may be accessed as a file.

    >>> from plone.subrequest import subrequest
    >>> response = subrequest('/folder1/@@url')
    >>> response._wrote
    >>> response.outputBody()
    >>> response._wrote
    1
    >>> response.stdout.seek(0, 0) or 0  # Py2 returns None, Py3 returns new position
    0
    >>> list(response.stdout)
    ['http://nohost/folder1']

Relative paths
--------------

.. test-case: relative

Relative paths are resolved relative to the parent request's location:

    >>> from plone.subrequest.tests import traverse
    >>> request = traverse('/folder1/@@test')
    >>> response = subrequest('folder1A/@@url')
    >>> response.getBody()
    b'http://nohost/folder1/folder1A'

.. test-case: relative-default-view

This takes account of default view's url.

    >>> request = traverse('/folder1')
    >>> request['URL'] == 'http://nohost/folder1/@@test'
    True
    >>> response = subrequest('folder1A/@@url')
    >>> response.getBody()
    b'http://nohost/folder1/folder1A'

Virtual hosting
---------------

.. test-case: virtual-hosting

When virtual hosting is used, absolute paths are traversed from the virtual host root.

    >>> request = traverse('/VirtualHostBase/http/nohost:80/folder1/VirtualHostRoot/')
    >>> response = subrequest('/folder1A/@@url')
    >>> response.getBody()
    b'http://nohost/folder1A'

Specifying the root
-------------------

.. test-case: specify-root

You may also set the root object explicitly

    >>> app = layer['app']
    >>> response = subrequest('/folder1A/@@url', root=app.folder1)
    >>> response.getBody()
    b'http://nohost/folder1/folder1A'

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

Or might raise an error rendered by a custom error view.

    >>> response = subrequest('/@@custom-error')
    >>> response.status
    500
    >>> response.body
    b'Custom exception occurred: A custom error'

.. test-case: status-ok

So check for the expected status.

    >>> response = subrequest('/')
    >>> response.status == 200
    True

Handling subrequests
--------------------

The parent request is set as PARENT_REQUEST onto subrequests.

Subrequests also provide the ``plone.subrequest.interfaces.ISubRequest``
marker interface.
