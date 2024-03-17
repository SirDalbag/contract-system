from rest_framework import status
from rest_framework.serializers import Serializer
from django.http import HttpRequest, JsonResponse
from django.db.models import QuerySet
from django.utils import timezone
from django.db.models import Model
from django.contrib.auth.models import User
from django_app import models
import datetime
import json


def get_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return (
        x_forwarded_for.split(",")[0]
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR")
    )


def timeout(user: User | None = None, limit: int = 10, seconds: int = 1) -> callable:
    def decorator(func: callable) -> callable:
        def wrapper(request: HttpRequest, *args: any, **kwargs: any) -> any:
            ip = get_ip(request)
            time = timezone.now() - datetime.timedelta(seconds=seconds)
            count = (
                models.Log.objects.filter(user=user, date__gt=time).count()
                if user
                else models.Log.objects.filter(ip=ip, date__gt=time).count()
            )
            if count > limit:
                return JsonResponse(
                    data={"message": "Too many attempts!"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            log = models.Log.objects.create(user=user, ip=ip, date=timezone.now())
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def serialization(
    model: Model,
    serializer: Serializer,
    filter: dict[str] = None,
    sort: str = None,
    **kwargs: any
) -> any:
    objects = model.objects.filter(**kwargs) if kwargs else model.objects.all()
    if filter:
        objects = objects.filter(**json.loads(filter))
    if sort:
        objects = objects.order_by(*sort.split(","))
    return serializer(
        objects,
        many=isinstance(objects, QuerySet),
    ).data
