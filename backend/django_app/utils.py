from rest_framework import status
from django.http import JsonResponse
from django.db.models import QuerySet
from django.utils import timezone
from django_app import models
import datetime
import json


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return (
        x_forwarded_for.split(",")[0]
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR")
    )


def timeout(user=None, limit=10, seconds=1):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            ip = get_ip(request)
            time = timezone.now() - datetime.timedelta(seconds=seconds)
            log = models.Log.objects.create(user=user, ip=ip, date=timezone.now())
            count = models.Log.objects.filter(ip=ip, date__gt=time).count()
            if count > limit:
                return JsonResponse(
                    data={"message": "Too many attempts!"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


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
