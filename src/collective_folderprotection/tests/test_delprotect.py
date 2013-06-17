# -*- coding: utf-8 -*-
import unittest2 as unittest

from AccessControl.unauthorized import Unauthorized

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective_folderprotection.testing import \
    COLLECTIVE_FOLDERPROTECTION_INTEGRATION_TESTING


class TestDelProtect(unittest.TestCase):

    layer = COLLECTIVE_FOLDERPROTECTION_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Create a folderish protected
        self.portal.invokeFactory('folderish_protected', 'protected')
        # And a folderish unprotected
        self.portal.invokeFactory('folderish_not_protected', 'not-protected')

    def test_not_allowed_to_remove(self):
        self.assertRaises(Unauthorized, self.portal.manage_delObjects, 'protected')
        self.assertIn('protected', self.portal)
        
    def test_allowed_to_remove(self):
        self.portal.manage_delObjects('not-protected')
        self.assertNotIn('not-protected', self.portal)
