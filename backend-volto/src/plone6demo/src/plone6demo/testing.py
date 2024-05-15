from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import plone6demo


class PLONE6DEMOLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=plone6demo)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plone6demo:default")
        applyProfile(portal, "plone6demo:initial")


PLONE6DEMO_FIXTURE = PLONE6DEMOLayer()


PLONE6DEMO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE6DEMO_FIXTURE,),
    name="PLONE6DEMOLayer:IntegrationTesting",
)


PLONE6DEMO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE6DEMO_FIXTURE, WSGI_SERVER_FIXTURE),
    name="PLONE6DEMOLayer:FunctionalTesting",
)


PLONE6DEMOACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONE6DEMO_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="PLONE6DEMOLayer:AcceptanceTesting",
)
