from plone import api
from plonedemo.site import _
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

import logging


logger = logging.getLogger(__name__)


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        return [
            "plondemo.site:uninstall",
            "plone.app.openid:default",
            "archetypes.multilingual:default",
        ]


def post_install(setup):
    """Post install script"""
    portal = api.portal.get()
    # We do not want the LRF and LIF created when installing p.a.m
    # because we'll import our own :)
    remove_content(portal)


def uninstall(setup):
    """Uninstall script"""


def remove_content(portal):
    default_content = [
        "front-page",
        "Members",
        "news",
        "events",
    ]
    for item in default_content:
        if item in portal:
            api.content.delete(portal[item])
