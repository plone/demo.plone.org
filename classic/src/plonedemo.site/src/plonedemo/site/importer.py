from plone import api
from zope.annotation.interfaces import IAnnotations
from plone.exportimport.importers.content import ContentImporter

ANNOTATIONS_KEY = "exportimport.annotations"


def global_obj_hook(item, obj):
    # Only run once
    if item["@type"] == "Plone Site":
        # This will be reset in post_handler of distributions
        api.portal.set_registry_record("plone.enable_link_integrity_checks", False)
    import_annotations(obj, item)
    return obj


class CustomContentImporter(ContentImporter):
    obj_hooks = [global_obj_hook]


def import_annotations(obj, item):
    # Required for mosaic tile settings
    annotations = IAnnotations(obj)
    for key in item.get(ANNOTATIONS_KEY, []):
        annotations[key] = item[ANNOTATIONS_KEY][key]
