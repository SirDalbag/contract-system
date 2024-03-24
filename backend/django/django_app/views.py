from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse
from django.core.cache import caches
from django.shortcuts import render
from django.db.models import Model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django_app import models, serializers, utils

Cache = caches["default"]


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def api(request: HttpRequest) -> Response:
    if request.method == "GET":
        return Response(data={"message": "OK"}, status=200)
    elif request.method == "POST":
        return Response(data={"message": request.data}, status=200)


@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def get_objects_or_object(
    request: HttpRequest,
    model: Model,
    serializer: Serializer,
    key: str,
    id: int | None = None,
) -> Response:
    if request.method == "GET":
        try:

            def get_data() -> ReturnList:
                return (
                    utils.serialization(model=model, serializer=serializer, id=id)
                    if id
                    else utils.serialization(
                        model=model,
                        serializer=serializer,
                        filter=request.GET.get("filter", None),
                        sort=request.GET.get("sort", None),
                    )
                )

            cache = utils.get_cache(key=key, cache=Cache, query=get_data, timeout=1)
            return Response(
                data={"data": utils.get_pagination(request=request, objects=cache)},
                status=200,
            )
        except Exception as error:
            return Response(data={"message": str(error)}, status=500)
    return Response(data={"message": "Method not allowed"}, status=405)


@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def get_objects_by_field(
    request: HttpRequest,
    model: Model,
    serializer: Serializer,
    field: dict[Model],
    id: int | None = None,
) -> Response:
    if request.method == "GET":
        try:
            key = list(field.keys())[0]

            def get_data() -> ReturnList:
                key = list(field.keys())[0]
                value = field[key].objects.get(id=id)
                return utils.serialization(
                    model=model,
                    serializer=serializer,
                    **{key: value},
                )

            objects = get_data()
            cache = utils.get_cache(
                key=f"contracts-{key}",
                cache=Cache,
                query=get_data,
                timeout=1,
            )
            return Response(
                data={
                    "data": utils.get_pagination(request=request, objects=cache),
                    "total_count": len(objects),
                },
                status=200,
            )
        except Exception as error:
            return Response(data={"message": str(error)}, status=400)
    return Response(data={"message": "Method not allowed"}, status=405)


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def post_object(request: HttpRequest, serializer: Serializer) -> Response:
    if request.method == "POST":
        try:
            serializer = serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"data": serializer.data}, status=201)
            return Response(data={"message": serializer.errors}, status=400)
        except Exception as error:
            return Response(data={"message": str(error)}, status=500)
    return Response(data={"message": "Method not allowed"}, status=405)


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def post_contract(request: HttpRequest) -> Response:
    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                author = request.user
            else:
                author, _ = User.objects.get_or_create(username="Anonymous")
            agent = models.Agent.objects.get(id=request.POST.get("id", None))
            comment = models.Comment.objects.create(
                comment=request.POST.get("comment", None)
            )
            total = request.POST.get("total", None)
            file = request.FILES.get("file_path", None)
            contract = models.Contract.objects.create(
                author=author,
                agent_id=agent,
                comment_id=comment,
                total=total,
                file_path=file,
            )
            return Response(
                data={
                    "data": serializers.ContractSerializer(contract, many=False).data
                },
                status=201,
            )
        except Exception as error:
            return Response(data={"message": str(error)}, status=400)
    return Response(data={"message": "Method not allowed"}, status=405)


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def register(request) -> Response:
    if request.method == "POST":
        try:
            username = request.data.get("username", None)
            password = request.data.get("password", None)
            if username and password and utils.check_password(password=password):
                User.objects.create(username=username, password=make_password(password))
                return Response(data={"message": "Account created"}, status=201)
            else:
                return Response(
                    data={"message": "Invalid login or password"},
                    status=401,
                )
        except Exception as error:
            return Response(data={"message": str(error)}, status=400)
    return Response(data={"message": "Method not allowed"}, status=405)
