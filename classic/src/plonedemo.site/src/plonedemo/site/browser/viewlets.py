from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets.common import ViewletBase

import pkg_resources
import sys


class FrontpageViewlet(ViewletBase):
    """The frontpage as a viewlet."""

    def show(self):
        context_state = api.content.get_view(
            "plone_context_state", self.context, self.request
        )
        if INavigationRoot.providedBy(context_state.canonical_object()):
            return context_state.is_view_template()

    def get_python_version(self):
        return f"{sys.version_info[0]}.{sys.version_info[1]}"

    def get_plone_version(self):
        try:
            version = pkg_resources.get_distribution("Plone").version
        except pkg_resources.DistributionNotFound:
            version = pkg_resources.get_distribution("Products.CMFPlone").version
        # Drop the trailing .0 in Products.CMFPlone versions
        # to get 5.2 instead of 5.2.0. Keep 5.0 and 6.0 intact.
        if len(version) > 3 and version.endswith(".0"):
            version = version[:-2]
        return version

    def reset_hours(self):
        return "4"


class VersionsViewlet(ViewletBase):
    def show(self):
        context_state = api.content.get_view(
            "plone_context_state", self.context, self.request
        )
        if INavigationRoot.providedBy(context_state.canonical_object()):
            return context_state.is_view_template()

    def version_overview(self):
        portal = api.portal.get()
        view = api.content.get_view("overview-controlpanel", portal, self.request)
        return view.version_overview()

    def portal_created(self):
        portal = api.portal.get()
        created_utc = portal.created().toZone("UTC")
        localized = api.portal.get_localized_time(created_utc, long_format=True)
        return f"{localized} UTC"
