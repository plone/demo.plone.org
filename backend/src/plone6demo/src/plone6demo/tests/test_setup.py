"""Setup tests for this package."""
from plone import api
from plone6demo.testing import PLONE6DEMO_INTEGRATION_TESTING  # noqa: E501
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that plone6demo is properly installed."""

    layer = PLONE6DEMO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup = self.portal.portal_setup
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if plone6demo is installed."""
        self.assertTrue(self.installer.is_product_installed("plone6demo"))

    def test_browserlayer(self):
        """Test that IPLONE6DEMOLayer is registered."""
        from plone6demo.interfaces import IPLONE6DEMOLayer
        from plone.browserlayer import utils

        self.assertIn(IPLONE6DEMOLayer, utils.registered_layers())

    def test_latest_version(self):
        """Test latest version of default profile."""
        self.assertEqual(
            self.setup.getLastVersionForProfile("plone6demo:default")[0],
            "20221212001",
        )


class TestUninstall(unittest.TestCase):

    layer = PLONE6DEMO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("plone6demo")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if plone6demo is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("plone6demo"))

    def test_browserlayer_removed(self):
        """Test that IPLONE6DEMOLayer is removed."""
        from plone6demo.interfaces import IPLONE6DEMOLayer
        from plone.browserlayer import utils

        self.assertNotIn(IPLONE6DEMOLayer, utils.registered_layers())
