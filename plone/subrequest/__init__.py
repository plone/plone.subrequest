from Acquisition import aq_base
from ZPublisher.BaseRequest import RequestContainer
from ZPublisher.Publish import dont_publish_class
from ZPublisher.Publish import missing_name
from ZPublisher.mapply import mapply
from cStringIO import StringIO
from posixpath import normpath
from urlparse import urlsplit, urljoin
from zope.globalrequest import getRequest, setRequest

__all__ = ['subrequest']

# http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html
CONDITIONAL_HEADERS = [
    'HTTP_IF_MODIFIED_SINCE',
    'HTTP_IF_UNMODIFIED_SINCE',
    'HTTP_IF_MATCH',
    'HTTP_IF_NONE_MATCH',
    'HTTP_IF_RANGE',
    ]

def subrequest(path, stdout=None):
    _, _, path, query, _ = urlsplit(path)

    parent_request = getRequest()
    here = '/'.join(parent_request._steps)
    path = urljoin(here, path)
    path = normpath(path)
    parent_app = parent_request.PARENTS[-1]
    parent_published = parent_request.get('PUBLISHED')
    request = parent_request.clone()
    try:
        setRequest(request)
        request_container = RequestContainer(REQUEST=request)
        app = aq_base(parent_app).__of__(request_container)
        request['PARENTS'] = [app]
        response = request.response
        response.stderr = None # only used on retry it seems
        if stdout is None:
            stdout = StringIO() # It might be possible to optimize this
        response.stdout = stdout
        response.write = stdout.write # the write method is non standard
        environ = request.environ
        environ['PATH_INFO'] = path
        environ['QUERY_STRING'] = query
        # Clean up the request.
        for header in CONDITIONAL_HEADERS:
            environ.pop(header, None)
        traversed = request.traverse(path)
        request.processInputs()
        result = mapply(traversed, positional=request.args,
                        keyword=request,
                        debug=None,
                        maybe=1,
                        missing_name=missing_name,
                        handle_class=dont_publish_class,
                        context=request,
                        bind=1)
        if result is not response:
            response.setBody(result)
        return response
    finally:
        request.clear()
        setRequest(parent_request)
