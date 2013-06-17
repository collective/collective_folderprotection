# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class CollectivefolderprotectionLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.folderprotection
        xmlconfig.file(
            'configure.zcml',
            collective.folderprotection,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.folderprotection:test_fixture')
        
        # Create a manager user
        pas = portal['acl_users']
        pas.source_users.addUser(
                'manager',
                'manager',
                'manager')
        pas.portal_role_manager.doAssignRoleToPrincipal('manager', 'Manager')
        
        # Create a contributor user
        pas = portal['acl_users']
        pas.source_users.addUser(
                'contributor',
                'contributor',
                'contributor')
        pas.portal_role_manager.doAssignRoleToPrincipal('contributor', 'Contributor')


COLLECTIVE_FOLDERPROTECTION_FIXTURE = CollectivefolderprotectionLayer()
COLLECTIVE_FOLDERPROTECTION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_FOLDERPROTECTION_FIXTURE,),
    name="CollectivefolderprotectionLayer:Integration"
)
COLLECTIVE_FOLDERPROTECTION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_FOLDERPROTECTION_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectivefolderprotectionLayer:Functional"
)
