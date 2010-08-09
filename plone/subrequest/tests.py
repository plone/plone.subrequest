import unittest2 as unittest
from plone.testing import Layer, z2, zodb

class PloneSubrequestFixture(Layer):
    defaultBases = (z2.STARTUP,)

    def setUp(self):
        context = self['configurationContext']
        

    def tearDown(self):
        pass

PLONESUBREQUEST_FIXTURE = PloneSubrequestFixture()

PLONESUBREQUEST_INTEGRATION_TESTING = z2.IntegrationTesting(bases=(PLONESUBREQUEST_FIXTURE,), name="PloneSubrequest:Integration")
MPLONESUBREQUEST_FUNCTIONAL_TESTING = z2.FunctionalTesting(bases=(PLONESUBREQUEST_FIXTURE,), name="PloneSubrequest:Functional")

class PloneSubrequestTests(unittest.TestCase):
    layer = PLONESUBREQUEST_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']

    def tearDown(self):
        pass

    def test_it_works(self):
        self.assertEqual(1,1)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
