import OFS.Folder
from Products.Five.browser import BrowserView
from five.localsitemanager import make_site
from plone.subrequest import subrequest
from plone.testing import Layer, z2, zodb, zca
from zope.globalrequest import getRequest, setRequest


class URLView(BrowserView):
    def __call__(self):
        return self.context.absolute_url()


class ResponseWriteView(BrowserView):
    def __call__(self):
        response = self.request.response
        response.write('Some data.\n')
        response.write('Some more data.\n')


class ErrorView(BrowserView):
    def __call__(self):
        raise Exception('An error')


class RootView(BrowserView):
    def __call__(self):
        return 'Root: %s' % self.context.absolute_url()


class SubrequestView(BrowserView):
    def __call__(self):
        url = self.request.form.get('url')
        if url is None:
            return 'Expected a url'
        response = subrequest(url)
        return response.body


def singleton(cls):
    return cls()

@singleton
class PLONE_SUBREQEST_FIXTURE(Layer):
    defaultBases = (z2.STARTUP,)

    def setUp(self):
        # Stack a new DemoStorage on top of the one from z2.STARTUP.
        self['zodbDB'] = zodb.stackDemoStorage(self.get('zodbDB'), name='PloneSubRequestFixture')

        # Create a new global registry
        zca.pushGlobalRegistry()
        self['configurationContext'] = context = zca.stackConfigurationContext(self.get('configurationContext'))

        # Load out ZCML
        from zope.configuration import xmlconfig
        import plone.subrequest
        xmlconfig.file('testing.zcml', plone.subrequest, context=context)

        with z2.zopeApp() as app:
            # Enable virtual hosting
            z2.installProduct(app, 'Products.SiteAccess')
            from Products.SiteAccess.VirtualHostMonster import VirtualHostMonster
            vhm = VirtualHostMonster()
            app._setObject(vhm.getId(), vhm, suppress_events=True)
            # With suppress_events=False, this is called twice...
            vhm.manage_afterAdd(vhm, app)
            # Setup default content
            app.manage_addFolder('folder1')
            make_site(app.folder1)
            app.folder1.manage_addFolder('folder1A')
            app.folder1.folder1A.manage_addFolder('folder1Ai')
            app.folder1.manage_addFolder('folder1B')
            app.manage_addFolder('folder2')
            make_site(app.folder2)
            app.folder2.manage_addFolder('folder2A')
            app.folder2.folder2A.manage_addFolder('folder2Ai space')

    def tearDown(self):
        # Zap the stacked configuration context
        zca.popGlobalRegistry()
        del self['configurationContext']

        # Zap the stacked ZODB
        self['zodbDB'].close()
        del self['zodbDB']


class PloneSubrequestLifecycle(z2.IntegrationTesting):
    def testSetUp(self):
        super(PloneSubrequestLifecycle, self).testSetUp()
        request = self['request']
        request['PARENTS'] = [self['app']]
        setRequest(request)

    def testTearDown(self):
        super(PloneSubrequestLifecycle, self).testTearDown()
        setRequest(None)


INTEGRATION_TESTING = PloneSubrequestLifecycle(bases=(PLONE_SUBREQEST_FIXTURE,), name="PloneSubrequest:Integration")
FUNCTIONAL_TESTING = z2.FunctionalTesting(bases=(PLONE_SUBREQEST_FIXTURE,), name="PloneSubrequest:Functional")

