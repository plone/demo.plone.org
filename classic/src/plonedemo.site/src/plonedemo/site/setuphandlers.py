from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.globalrequest import getRequest
from zope.interface import alsoProvides
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProducts(self):
        return ["plone.volto"]


def pre_install(answers):
    try:
        from collective.tiles.carousel.interfaces import ICollectiveTilesCarouselLayer
        request = getRequest()
        alsoProvides(request, ICollectiveTilesCarouselLayer)
    except ImportError:
        pass
    return answers

def post_install(distribution, site, answers):
    """Post install script for distribution."""
    api.portal.set_registry_record("plone.enable_link_integrity_checks", True)
    site.setLayout("language-switcher")
    return site
