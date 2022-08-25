from five.localsitemanager import make_site
from plone.subrequest import subrequest
from plone.testing import Layer
from plone.testing import zca
from plone.testing import zodb
from plone.testing import zope
from Products.Five.browser import BrowserView
from zope.globalrequest import setRequest


class CustomException(Exception):
    """Custom exception"""


class CustomExceptionHandler(BrowserView):
    def __call__(self):
        self.request.response.setStatus(500)
        return f"Custom exception occurred: {self.context}"


class CookieView(BrowserView):
    def __call__(self):
        response = self.request.response
        response.setCookie("cookie_name", "cookie_value")


class ParameterView(BrowserView):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.keys = self.request.keys()

    def __call__(self):
        return str(self.keys)


class URLView(BrowserView):
    def __call__(self):
        url = self.context.absolute_url()
        return url


class ResponseWriteView(BrowserView):
    def __call__(self):
        response = self.request.response
        response.write("Some data.\n")
        response.write("Some more data.\n")


class ErrorView(BrowserView):
    def __call__(self):
        raise Exception("An error")


class CustomErrorView(BrowserView):
    def __call__(self):
        raise CustomException("A custom error")


class RootView(BrowserView):
    def __call__(self):
        return f"Root: {self.context.absolute_url()}"


class SubrequestView(BrowserView):
    def __call__(self):
        url = self.request.form.get("url")
        if url is None:
            return "Expected a url"
        response = subrequest(url)
        return response.body


class StreamIteratorView(BrowserView):
    def __call__(self):
        from ZServer.tests.test_responses import test_streamiterator

        response = self.request.response
        response.setHeader("content-length", 5)
        return test_streamiterator()


class FileStreamIteratorView(BrowserView):
    def __call__(self):
        from pkg_resources import resource_filename
        from ZPublisher.Iterators import filestream_iterator

        filename = resource_filename("plone.subrequest", "testfile.txt")
        return filestream_iterator(filename)


def singleton(cls):
    return cls()


@singleton
class PLONE_SUBREQEST_FIXTURE(Layer):
    defaultBases = (zope.STARTUP,)

    def setUp(self):
        # Stack a new DemoStorage on top of the one from zope.STARTUP.
        self["zodbDB"] = zodb.stackDemoStorage(
            self.get("zodbDB"), name="PloneSubRequestFixture"
        )

        # Create a new global registry
        zca.pushGlobalRegistry()
        self["configurationContext"] = context = zca.stackConfigurationContext(
            self.get("configurationContext")
        )

        # Load out ZCML
        from zope.configuration import xmlconfig

        import plone.subrequest

        xmlconfig.file("testing.zcml", plone.subrequest, context=context)

        with zope.zopeApp() as app:
            # Enable virtual hosting
            zope.installProduct(app, "Products.SiteAccess")
            from Products.SiteAccess.VirtualHostMonster import VirtualHostMonster

            vhm = VirtualHostMonster()
            app._setObject(vhm.getId(), vhm, suppress_events=True)
            # With suppress_events=False, this is called twice...
            vhm.manage_afterAdd(vhm, app)
            # Setup default content
            app.manage_addFolder("folder1")
            make_site(app.folder1)
            app.folder1.manage_addFolder("folder1A")
            app.folder1.folder1A.manage_addFolder("folder1Ai")
            app.folder1.manage_addFolder("folder1B")
            app.manage_addFolder("folder2")
            make_site(app.folder2)
            app.folder2.manage_addFolder("folder2A")
            app.folder2.folder2A.manage_addFolder("folder2Ai space")

    def tearDown(self):
        # Zap the stacked configuration context
        zca.popGlobalRegistry()
        del self["configurationContext"]

        # Zap the stacked ZODB
        self["zodbDB"].close()
        del self["zodbDB"]


class PloneSubrequestLifecycle(zope.IntegrationTesting):
    def testSetUp(self):
        super().testSetUp()
        request = self["request"]
        request["PARENTS"] = [self["app"]]
        setRequest(request)

    def testTearDown(self):
        super().testTearDown()
        setRequest(None)


INTEGRATION_TESTING = PloneSubrequestLifecycle(
    bases=(PLONE_SUBREQEST_FIXTURE,), name="PloneSubrequest:Integration"
)
FUNCTIONAL_TESTING = zope.FunctionalTesting(
    bases=(PLONE_SUBREQEST_FIXTURE,), name="PloneSubrequest:Functional"
)
