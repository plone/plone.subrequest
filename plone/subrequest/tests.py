import unittest2 as unittest
from plone.testing import Layer, zodb, zca, z2
from plone.subrequest import subrequest
from zope.globalrequest import setRequest

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
        import plone.subrequest
        xmlconfig.file('configure.zcml', plone.subrequest, context=context)

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
        del self.request

    def test_it_works(self):
        response = subrequest('/acl_users')
        self.assertEqual(response.body, '<UserFolder at acl_users>')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
