from django.db.models import QuerySet
import json


def serialization(model, serializer, filter=None, sort=None, **kwargs):
    objects = model.objects.filter(**kwargs) if kwargs else model.objects.all()
    if filter:
        objects = objects.filter(**json.loads(filter))
    if sort:
        objects = objects.order_by(*sort.split(","))
    return serializer(
        objects,
        many=isinstance(objects, QuerySet),
    ).data
