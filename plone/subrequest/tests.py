import manuel.doctest
import manuel.testcase
import manuel.testing
import unittest2 as unittest
from plone.testing import Layer, layered, z2, zodb, zca

from Products.Five.browser import BrowserView
from plone.subrequest import subrequest
from zope.globalrequest import setRequest

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


class TestView(BrowserView):
    def __call__(self):
        url = self.request.form.get('url')
        if url is None:
            return 'No url parameter supplied.'
        response = subrequest(url)
        return response.body


class Fixture(Layer):
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
            app.folder1.manage_addFolder('folder1A')
            app.folder1.folder1A.manage_addFolder('folder1Ai')
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


FIXTURE = Fixture()
INTEGRATION_TESTING = z2.IntegrationTesting(bases=(FIXTURE,), name="PloneSubrequest:Integration")
FUNCTIONAL_TESTING = z2.FunctionalTesting(bases=(FIXTURE,), name="PloneSubrequest:Functional")


class FunctionalTests(unittest.TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.browser = z2.Browser(self.layer['app'])

    def test_absolute(self):
        self.browser.open('http://nohost/folder1/@@url')
        self.assertEqual(self.browser.contents, 'http://nohost/folder1')

    def test_virtual_hosting(self):
        parts = ('folder1', 'folder1A/@@url')
        expect = 'folder1A'
        url = "http://nohost/VirtualHostBase/http/example.org:80/%s/VirtualHostRoot/_vh_fizz/_vh_buzz/_vh_fizzbuzz/%s" % parts
        expect_url = 'http://example.org/fizz/buzz/fizzbuzz/%s' % expect
        self.browser.open(url)
        self.assertEqual(self.browser.contents, expect_url)

    def test_virtual_hosting_relative(self):
        parts = ('folder1', 'folder1A?url=folder1Ai/@@url')
        expect = 'folder1A/folder1Ai'
        url = "http://nohost/VirtualHostBase/http/example.org:80/%s/VirtualHostRoot/_vh_fizz/_vh_buzz/_vh_fizzbuzz/%s" % parts
        expect_url = 'http://example.org/fizz/buzz/fizzbuzz/%s' % expect
        self.browser.open(url)
        self.assertEqual(self.browser.contents, expect_url)

    def test_virtual_hosting_absolute(self):
        parts = ('folder1', 'folder1A?url=/folder1B/@@url')
        expect = 'folder1B'
        url = "http://nohost/VirtualHostBase/http/example.org:80/%s/VirtualHostRoot/_vh_fizz/_vh_buzz/_vh_fizzbuzz/%s" % parts
        expect_url = 'http://example.org/fizz/buzz/fizzbuzz/%s' % expect
        self.browser.open(url)
        self.assertEqual(self.browser.contents, expect_url)


class IntegrationBase(object):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = app = self.layer['app']
        self.request = request = self.layer['request']
        request['PARENTS'] = [app]
        setRequest(request)

    def tearDown(self):
        setRequest(None)    


class IntegrationTests(IntegrationBase, unittest.TestCase):

    def test_absolute(self):
        response = subrequest('/folder1/@@url')
        self.assertEqual(response.body, 'http://nohost/folder1')

    def test_absolute_query(self):
        response = subrequest('/folder1/folder1A?url=/folder2/folder2A/@@url')
        self.assertEqual(response.body, 'http://nohost/folder2/folder2A')

    def test_relative(self):
        response = subrequest('/folder1?url=folder1B/@@url')
        # /folder1 resolves to /folder1/@@test
        self.assertEqual(response.body, 'http://nohost/folder1/folder1B')

    def test_root(self):
        response = subrequest('/')
        self.assertEqual(response.body, 'Root: http://nohost')

    def test_virtual_hosting(self):
        url = "/VirtualHostBase/http/example.org:80/%s/VirtualHostRoot/_vh_fizz/_vh_buzz/_vh_fizzbuzz/%s" % ('folder1', 'folder1A/@@url')
        response = subrequest(url)
        self.assertEqual(response.body, 'http://example.org/fizz/buzz/fizzbuzz/folder1A')

    def test_virtual_hosting_relative(self):
        url = "/VirtualHostBase/http/example.org:80/%s/VirtualHostRoot/_vh_fizz/_vh_buzz/_vh_fizzbuzz/%s" % ('folder1', 'folder1A?url=folder1B/@@url')
        response = subrequest(url)
        self.assertEqual(response.body, 'http://example.org/fizz/buzz/fizzbuzz/folder1B')

    def test_not_found(self):
        response = subrequest('/notfound')
        self.assertEqual(response.status, 404)

    def test_virtual_host_root(self):
        parts = ('folder1', 'folder1A/@@url')
        url = "/VirtualHostBase/http/example.org:80/%s/VirtualHostRoot/_vh_fizz/_vh_buzz/_vh_fizzbuzz/%s" % parts
        self.request.traverse(url)
        self.request['PATH_INFO'] = url
        response = subrequest('/folder1B/@@url')
        self.assertEqual(response.body, 'http://example.org/fizz/buzz/fizzbuzz/folder1B')

    def test_virtual_host_root_with_root(self):
        parts = ('folder1', 'folder1A/@@url')
        url = "/VirtualHostBase/http/example.org:80/%s/VirtualHostRoot/_vh_fizz/_vh_buzz/_vh_fizzbuzz/%s" % parts
        self.request.traverse(url)
        self.request['PATH_INFO'] = url
        response = subrequest('/folder1Ai/@@url', root=self.app.folder1.folder1A)
        self.assertEqual(response.body, 'http://example.org/fizz/buzz/fizzbuzz/folder1A/folder1Ai')

    def test_subrequest_root(self):
        response = subrequest('/folder1Ai/@@url', root=self.app.folder1.folder1A)
        self.assertEqual(response.body, 'http://nohost/folder1/folder1A/folder1Ai')



def test_suite():
    class DocTestCase(IntegrationBase, manuel.testing.TestCase):
        pass
    
    suite = unittest.defaultTestLoader.loadTestsFromName(__name__)
    m = manuel.doctest.Manuel()
    #m += manuel.testcase.SectionManuel() # too many
    m += manuel.testcase.MarkerManuel()
    suite.addTest(manuel.testing.TestSuite(m, '../../README.txt', TestCase=DocTestCase, globs=dict(subrequest=subrequest)))
    return suite