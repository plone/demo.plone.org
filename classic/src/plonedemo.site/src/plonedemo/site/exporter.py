from plone.exportimport.exporters.content import ContentExporter
from plone.restapi.interfaces import IJsonCompatible
from zope.annotation.interfaces import IAnnotations


ANNOTATIONS_TO_EXPORT = [
    # None yet
]

ANNOTATIONS_KEY = "exportimport.annotations"


def global_dict_hook(item, obj, config):
    item = export_annotations(item, obj)
    return item


def export_annotations(item, obj):
    results = {}
    annotations = IAnnotations(obj)
    for key in annotations:
        if key in ANNOTATIONS_TO_EXPORT or key.startswith("plone.tiles"):
            data = annotations.get(key)
            if data:
                results[key] = IJsonCompatible(data, None)
    if results:
        item[ANNOTATIONS_KEY] = results
    return item


class CustomContentExporter(ContentExporter):
    data_hooks = [
        global_dict_hook,
    ]
