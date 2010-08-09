import unittest2 as unittest
from Products.Five.browser import BrowserView
from plone.testing import Layer, zodb, zca, z2
from plone.subrequest import subrequest
from zope.globalrequest import setRequest

TEST_ZCML = """\
<configure xmlns="http://namespaces.zope.org/zope" xmlns:browser="http://namespaces.zope.org/browser">
    <include package="plone.subrequest" />
    <browser:page 
        name="test.html"
        for="OFS.Folder.Folder"
        class="plone.subrequest.tests.TestView"
        permission="zope.Public"
        />
    <browser:page 
        name="url.html"
        for="OFS.Folder.Folder"
        class="plone.subrequest.tests.URLView"
        permission="zope.Public"
        />
    <browser:defaultView
        for="OFS.Folder.Folder"
        name="url.html"
        />
</configure>
"""

class URLView(BrowserView):
    def __call__(self):
        return self.context.absolute_url()

class TestView(BrowserView):
    def __call__(self):
        url = self.request.get('url')
        response = subrequest(url)
        return response.body

class PloneSubrequestFixture(Layer):
    defaultBases = (z2.STARTUP,)

    def setUp(self):
        # Stack a new DemoStorage on top of the one from z2.STARTUP.
        self['zodbDB'] = zodb.stackDemoStorage(self.get('zodbDB'), name='PloneSubRequestFixture')

        # Create a new global registry
        zca.pushGlobalRegistry()
        self['configurationContext'] = context = zca.stackConfigurationContext(self.get('configurationContext'))

        # Load out ZCML
        from zope.configuration import xmlconfig
        xmlconfig.string(TEST_ZCML, context=context)

        # Setup default content
        with z2.zopeApp() as app:
            app.manage_addFolder('folder1')
            app.folder1.manage_addFolder('folder1A')
            app.folder1.manage_addFolder('folder1B')
            app.manage_addFolder('folder2')
            app.folder2.manage_addFolder('folder2A')

    def tearDown(self):
        # Zap the stacked configuration context
        zca.popGlobalRegistry()
        del self['configurationContext']

        # Zap the stacked ZODB
        self['zodbDB'].close()
        del self['zodbDB']


PLONESUBREQUEST_FIXTURE = PloneSubrequestFixture()
PLONESUBREQUEST_INTEGRATION_TESTING = z2.IntegrationTesting(bases=(PLONESUBREQUEST_FIXTURE,), name="PloneSubrequest:Integration")
PLONESUBREQUEST_FUNCTIONAL_TESTING = z2.FunctionalTesting(bases=(PLONESUBREQUEST_FIXTURE,), name="PloneSubrequest:Functional")


class PloneSubrequestTests(unittest.TestCase):
    layer = PLONESUBREQUEST_INTEGRATION_TESTING

    def setUp(self):
        self.app = app = self.layer['app']
        self.request = request = self.layer['request']
        request['PARENTS'] = [app]
        setRequest(request)

    def tearDown(self):
        setRequest(None)

    def test_absolute(self):
        response = subrequest('/folder1/folder1A')
        self.assertEqual(response.body, 'http://nohost/folder1/folder1A')

    def test_absolute_query(self):
        response = subrequest('/folder1/folder1A/@@test.html?url=/folder2/folder2A')
        self.assertEqual(response.body, 'http://nohost/folder2/folder2A')

    def test_relative(self):
        response = subrequest('/folder1/folder1A/@@test.html?url=folder1B')
        self.assertEqual(response.body, 'http://nohost/folder1/folder1B')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
