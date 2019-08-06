# -*- coding: utf-8 -*-
from collective_folderprotection.testing import (
    COLLECTIVE_FOLDERPROTECTION_FUNCTIONAL_TESTING,
)
from plone.testing import layered
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                robotsuite.RobotTestSuite("manager_functional.robot"),
                layer=COLLECTIVE_FOLDERPROTECTION_FUNCTIONAL_TESTING,
            )
        ]
    )
    suite.addTests(
        [
            layered(
                robotsuite.RobotTestSuite("owner_functional.robot"),
                layer=COLLECTIVE_FOLDERPROTECTION_FUNCTIONAL_TESTING,
            )
        ]
    )
    suite.addTests(
        [
            layered(
                robotsuite.RobotTestSuite("member_functional.robot"),
                layer=COLLECTIVE_FOLDERPROTECTION_FUNCTIONAL_TESTING,
            )
        ]
    )
    return suite
