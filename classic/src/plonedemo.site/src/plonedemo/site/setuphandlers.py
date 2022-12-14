from plone import api
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.multilingual.interfaces import ITranslationManager
from plone.app.textfield.value import RichTextValue
from plonedemo.site import _
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.interfaces import ILanguage
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.utils import bodyfinder
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer

import logging
import os


logger = logging.getLogger(__name__)

DEFAULT_EMAIL = "demo@plone.de"
FRONTPAGE_TITLE = _("Welcome to Plone")
FRONTPAGE_DESCRIPTION = _("The ultimate Open Source Enterprise CMS")
IMPORTED_FOLDER_ID = "demo"


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
    remove_content(portal)
    create_demo_users()
    languages = api.portal.get_registry_record("plone.available_languages")
    ml_setup_tool = SetupMultilingualSite()
    ml_setup_tool.setupSite(portal)
    for language in languages:
        container = portal[language]

        # Create frontpage for language
        frontpage = create_frontpage(
            portal, container=container, target_language=language
        )
        container.setDefaultPage("frontpage")
        ILanguage(frontpage).set_language(language)

        # Link the new frontpage as a translation to all existing items
        for lang in languages:
            existing_frontpage = portal[lang].get("frontpage")
            if existing_frontpage:
                ITranslationManager(existing_frontpage).register_translation(
                    language, frontpage
                )

        # Import zexp for language
        import_zexp(
            setup,
            filename=f"py3demo_{language}.zexp",
            container=container,
            name="demo",
            update=True,
            publish=True,
        )

    default_language = api.portal.get_default_language()
    default_lang_folder = portal.get(default_language)
    demo_folder = default_lang_folder.get(IMPORTED_FOLDER_ID)
    for language in languages:
        if not demo_folder:
            break
        if language == default_language:
            continue
        lang_folder = portal.get(language)
        lang_demo_folder = lang_folder.get(IMPORTED_FOLDER_ID)
        if not lang_demo_folder:
            continue

        # link demo-folders
        link_translations(
            obj=demo_folder, translation=lang_demo_folder, language=language
        )

        translated = []
        for obj1_id, obj1 in demo_folder.contentItems():
            # try to find a possible translation
            for obj2_id, obj2 in lang_demo_folder.contentItems():
                if obj2_id in translated:
                    continue
                # link the first item with the same portal_type
                if obj1.portal_type == obj2.portal_type:
                    link_translations(obj=obj1, translation=obj2, language=language)
                    translated.append(obj2_id)
                    break
    # setup_wpd(portal)


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


def create_demo_users():
    # Do something during the installation of this package
    demo_users = [
        {
            "login": "editor",
            "password": "ploneeditor",
            "fullname": "Editor",
            "roles": ("Reader", "Contributor", "Editor", "Member"),
        },
        {
            "login": "editorinchief",
            "password": "ploneeditorinchief",
            "fullname": "Editor-in-chief",
            "groups": ["Reviewers"],
            "roles": ("Reader", "Contributor", "Reviewer", "Editor", "Member"),
        },
        {
            "login": "manager",
            "password": "plonemanager",
            "fullname": "Manager",
            "groups": ["Administrators"],
            "roles": ("Administrator",),
        },
    ]
    for demo_user in demo_users:
        if api.user.get(username=demo_user.get("login")):
            continue
        new_user = api.user.create(
            email=DEFAULT_EMAIL,
            username=demo_user.get("login"),
            password=demo_user.get("password"),
            roles=demo_user.get("roles"),
            properties={"fullname": demo_user.get("fullname")},
        )
        for group in demo_user.get("groups", []):
            api.group.add_user(
                groupname=group,
                user=new_user,
            )


def create_frontpage(portal, container, target_language):
    """Create a frontpage. The text is the translation or default of
    the view '@@demo_frontpage'.
    """
    if not container.get("frontpage"):
        frontpage = api.content.create(
            container, "Document", "frontpage", FRONTPAGE_TITLE
        )
        api.content.transition(frontpage, to_state="published")
    frontpage = container.get("frontpage")
    util = queryUtility(ITranslationDomain, "plonedemo.site")
    frontpage.title = util.translate(FRONTPAGE_TITLE, target_language=target_language)
    frontpage.description = util.translate(
        FRONTPAGE_DESCRIPTION, target_language=target_language
    )
    front_text = None
    # Get frontpage-text from the translation-machinery.
    # To edit it you have to modify
    # plonedemo/site/locales/XX/LC_MESSAGES/plonedemo.site.po
    translated_text = util.translate(
        msgid="plonedemo_frontpage", target_language=target_language
    )
    if translated_text != "plonedemo_frontpage":
        front_text = translated_text
    if front_text is None:
        # Get text from reading the template-file since I can't find a way to
        # get the english default text using util.translate()
        # To modify edit plonedemo/site/browser/templates/frontpage.pt
        path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "browser",
            "templates",
            "frontpage.pt",
        )
        frontpage_raw = open(path).read()
        front_text = bodyfinder(frontpage_raw).strip()

    frontpage.text = RichTextValue(front_text, "text/html", "text/x-html-safe")
    return frontpage


def import_zexp(setup, filename, container, name, update=True, publish=True):
    """Import a zexp"""
    # Check if the zexp-file is actually in profiles/default
    context = setup._getImportContext("profile-plonedemo.site:default")
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "profiles", "default", filename
    )
    if filename not in context.listDirectory(path=None):
        logger.info(f"zexp-file {path} does not exist")
        return
    if name in container.keys():
        if not update:
            logger.info(f"Keeping {name}. Import of zexp aborted.")
            return
        else:
            logger.info(f"Purging {name}.")
            api.content.delete(container.get(name), check_linkintegrity=False)

    # Import zexp
    container._importObjectFromFile(str(path), verify=0)

    # publish all items!
    if publish:
        new = container[name]
        path = "/".join(new.getPhysicalPath())
        catalog = api.portal.get_tool("portal_catalog")
        for brain in catalog(path={"query": path, "depth": 2}):
            item = brain.getObject()
            try:
                api.content.transition(item, to_state="published")
            except WorkflowException:
                pass


def link_translations(obj, translation, language):
    if obj is translation or obj.language == language:
        logger.info(
            "Not linking {} to {} ({})".format(
                obj.absolute_url(), translation.absolute_url(), language
            )
        )
        return
    logger.info(
        "Linking {} to {} ({})".format(
            obj.absolute_url(), translation.absolute_url(), language
        )
    )
    ITranslationManager(obj).register_translation(language, translation)


# def setup_wpd(portal):
#     from datetime import date
#     qi = api.portal.get_tool('portal_quickinstaller')
#     qi.installProduct('wpd.countdown')
#     api.portal.set_registry_record('wpd.countdown.browser.views.IWPDSchema.wpd_date', date(year=2017, month=4, day=28))  # noqa
#     api.portal.set_registry_record('wpd.countdown.browser.views.IWPDSchema.wpd_url', 'http://plone.de/world-plone-day/')  # noqa
