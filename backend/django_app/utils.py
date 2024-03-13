from django.db.models import QuerySet

def serialization(model, serializer, sort = None, **kwargs):
    objects = model.objects.filter(**kwargs) if kwargs else model.objects.all()
    if sort:
        objects = objects.order_by(*sort.split(","))
    return serializer(
        objects,
        many=isinstance(objects, QuerySet),
    ).data