# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from mingtak.ECBase.testing import MINGTAK_ECBASE_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that mingtak.ECBase is properly installed."""

    layer = MINGTAK_ECBASE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if mingtak.ECBase is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'mingtak.ECBase'))

    def test_browserlayer(self):
        """Test that IMingtakEcbaseLayer is registered."""
        from mingtak.ECBase.interfaces import (
            IMingtakEcbaseLayer)
        from plone.browserlayer import utils
        self.assertIn(IMingtakEcbaseLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MINGTAK_ECBASE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['mingtak.ECBase'])

    def test_product_uninstalled(self):
        """Test if mingtak.ECBase is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'mingtak.ECBase'))

    def test_browserlayer_removed(self):
        """Test that IMingtakEcbaseLayer is removed."""
        from mingtak.ECBase.interfaces import \
            IMingtakEcbaseLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMingtakEcbaseLayer, utils.registered_layers())
