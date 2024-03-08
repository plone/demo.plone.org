from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProducts(self):
        return ["plone.volto"]


def post_install(distribution, site, answers):
    """Post install script for distribution."""
    site.setLayout("language-switcher")
    return site
