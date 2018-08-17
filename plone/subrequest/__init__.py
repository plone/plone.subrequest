# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from AccessControl.SecurityManagement import setSecurityManager
from Acquisition import aq_base
from logging import getLogger
from plone.subrequest.interfaces import ISubRequest
from plone.subrequest.subresponse import SubResponse
from posixpath import normpath
from six.moves import cStringIO as StringIO
from six.moves.urllib.parse import unquote
from six.moves.urllib.parse import urljoin
from six.moves.urllib.parse import urlsplit
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest
from zope.globalrequest import setRequest
from zope.interface import alsoProvides
from zope.site.hooks import getSite
from zope.site.hooks import setSite
from ZPublisher.BaseRequest import RequestContainer
from ZPublisher.mapply import mapply

import re
import six


try:
    from ZPublisher.WSGIPublisher import dont_publish_class
    from ZPublisher.WSGIPublisher import missing_name
except ImportError:
    from ZPublisher.Publish import dont_publish_class
    from ZPublisher.Publish import missing_name

try:
    from plone.protect.auto import SAFE_WRITE_KEY
    from plone.protect.interfaces import IDisableCSRFProtection
except ImportError:
    SAFE_WRITE_KEY = 'plone.protect.safe_oids'
    from zope.interface import Interface

    class IDisableCSRFProtection(Interface):
        pass


__all__ = ['subrequest', 'SubResponse']

# http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html
CONDITIONAL_HEADERS = [
    'HTTP_IF_MODIFIED_SINCE',
    'HTTP_IF_UNMODIFIED_SINCE',
    'HTTP_IF_MATCH',
    'HTTP_IF_NONE_MATCH',
    'HTTP_IF_RANGE',
    'HTTP_RANGE',  # Not strictly a conditional header, but scrub it anyway
]

OTHER_IGNORE = set([
    'ACTUAL_URL',
    'LANGUAGE_TOOL',
    'PARENTS',
    'PARENT_REQUEST',
    'PUBLISHED',
    'RESPONSE',
    'SERVER_URL',
    'TraversalRequestNameStack',
    'URL',
    'VIRTUAL_URL',
    'VIRTUAL_URL_PARTS',
    'VirtualRootPhysicalPath',
    'method',
    'traverse_subpath',
])

OTHER_IGNORE_RE = re.compile(r'^(?:BASE|URL)\d+$')

logger = getLogger('plone.subrequest')


def subrequest(url, root=None, stdout=None, exception_handler=None):
    assert url is not None, 'You must pass a url'
    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')
    _, _, path, query, _ = urlsplit(url)
    parent_request = getRequest()
    assert parent_request is not None, \
        'Unable to get request, perhaps zope.globalrequest is not configured.'
    parent_site = getSite()
    security_manager = getSecurityManager()
    parent_app = parent_request.PARENTS[-1]
    if path.startswith('/'):
        path = normpath(path)
        vurl_parts = parent_request.get('VIRTUAL_URL_PARTS')
        if vurl_parts is not None:
            # Use the virtual host root
            path_past_root = unquote(vurl_parts[-1])
            root_path = normpath(
                parent_request['PATH_INFO']
            ).rstrip('/')[:-len(path_past_root) or None]
            if root is None:
                path = root_path + path
            else:
                path = '{0}/{1}{2}'.format(
                    root_path,
                    root.virtual_url_path(),
                    path
                )
        elif root is not None:
            path = '/{0}{1}'.format(root.virtual_url_path(), path)
    else:
        try:
            parent_url = parent_request['URL']
            if isinstance(parent_url, six.binary_type):
                parent_url = parent_url.encode('utf-8')
            # extra is the hidden part of the url, e.g. a default view
            extra = unquote(
                parent_url[len(parent_request['ACTUAL_URL']):]
            )
        except KeyError:
            extra = ''
        here = parent_request['PATH_INFO'] + extra
        path = urljoin(here, path)
        path = normpath(path)
    request = parent_request.clone()
    for name, parent_value in parent_request.other.items():
        if name in OTHER_IGNORE \
           or OTHER_IGNORE_RE.match(name) \
           or name.startswith('_'):
            continue
        request.other[name] = parent_value
    for key, value in parent_request.response.cookies.items():
        request.cookies[key] = value['value']
    request['PARENT_REQUEST'] = parent_request
    alsoProvides(request, ISubRequest)
    try:
        setRequest(request)
        request_container = RequestContainer(REQUEST=request)
        app = aq_base(parent_app).__of__(request_container)
        request['PARENTS'] = [app]
        response = request.response
        response.__class__ = SubResponse
        response.stderr = None  # only used on retry it seems
        if stdout is None:
            stdout = StringIO()  # It might be possible to optimize this
        response.stdout = stdout
        environ = request.environ
        environ['PATH_INFO'] = path
        environ['QUERY_STRING'] = query
        # Clean up the request.
        for header in CONDITIONAL_HEADERS:
            environ.pop(header, None)
        try:
            request.processInputs()
            traversed = request.traverse(path)
            result = mapply(
                traversed,
                positional=request.args,
                keyword=request,
                debug=None,
                maybe=1,
                missing_name=missing_name,
                handle_class=dont_publish_class,
                context=request,
                bind=1
            )
            if result is not response:
                response.setBody(result)
            for key, value in request.response.cookies.items():
                parent_request.response.cookies[key] = value
        except Exception as e:
            logger.exception('Error handling subrequest to {0}'.format(url))
            if exception_handler is not None:
                exception_handler(response, e)
            else:
                view = queryMultiAdapter((e, request), name=u'index.html')
                if view is not None:
                    v = view()
                    response.setBody(v)
                else:
                    response.exception()
        return response
    finally:
        if SAFE_WRITE_KEY in request.environ:
            # append this list of safe oids to parent request
            if SAFE_WRITE_KEY not in parent_request.environ:
                parent_request.environ[SAFE_WRITE_KEY] = []
            new_keys = (
                set(request.environ[SAFE_WRITE_KEY]) -
                set(parent_request.environ[SAFE_WRITE_KEY])
            )
            parent_request.environ[SAFE_WRITE_KEY].extend(new_keys)
        if IDisableCSRFProtection.providedBy(request):
            alsoProvides(parent_request, IDisableCSRFProtection)
        request.clear()
        setRequest(parent_request)
        setSite(parent_site)
        setSecurityManager(security_manager)


def unauthorized_exception_handler(response, exception):
    """exception handler for subrequests delegating Unauthorized to a 401,
    but raising all other exceptions (resulting later in a 500).
    """
    if not isinstance(exception, Unauthorized):
        return response.exception()
    response.setStatus(401)
