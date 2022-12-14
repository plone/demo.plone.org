from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import plonedemo.site


class PlonedemoSiteLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)  # noqa: N815

    def setUpZope(self, app, configurationContext):  # noqa: N803
        self.loadZCML(package=plonedemo.site)

    def setUpPloneSite(self, portal):  # noqa: N803
        applyProfile(portal, "plonedemo.site:default")


PLONEDEMO_SITE_FIXTURE = PlonedemoSiteLayer()


PLONEDEMO_SITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEDEMO_SITE_FIXTURE,),
    name="PlonedemoSiteLayer:IntegrationTesting",
)


PLONEDEMO_SITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONEDEMO_SITE_FIXTURE,),
    name="PlonedemoSiteLayer:FunctionalTesting",
)


PLONEDEMO_SITE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONEDEMO_SITE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="PlonedemoSiteLayer:AcceptanceTesting",
)
