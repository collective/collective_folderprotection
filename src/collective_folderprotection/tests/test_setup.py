# -*- coding: utf-8 -*-
import unittest

from Products.CMFCore.utils import getToolByName

from plone.browserlayer.utils import registered_layers

from collective_folderprotection.config import PROJECTNAME

from collective_folderprotection.testing import (
    COLLECTIVE_FOLDERPROTECTION_INTEGRATION_TESTING,
)


class TestSetup(unittest.TestCase):

    layer = COLLECTIVE_FOLDERPROTECTION_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.qi_tool = getToolByName(self.portal, "portal_quickinstaller")

    def test_installed(self):
        qi = getattr(self.portal, "portal_quickinstaller")
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue(
            "IFolderProtectLayer" in layers, "add-on layer was not installed"
        )
