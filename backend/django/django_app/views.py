from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.cache import caches
from django.shortcuts import render
from django.db.models import Model
from django.contrib.auth.models import User
from django_app import models, serializers, utils
from django.views.decorators.csrf import csrf_exempt


Cache = caches["default"]


def get_cache(
    key: str, query: callable = lambda: any, timeout: int = 10, cache: any = Cache
) -> any:
    data = cache.get(key)
    if data is None:
        data = query()
        cache.set(key, data, timeout)
    return data


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def api(request: HttpRequest) -> Response:
    if request.method == "GET":
        return Response(data={"message": "OK"}, status=200)
    elif request.method == "POST":
        return Response(data={"message": request.data}, status=200)


@utils.timeout()
@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def get_objects_or_object(
    request: HttpRequest,
    model: Model,
    serializer: Serializer,
    key: str,
    id: int | None = None,
) -> Response:
    try:

        def get_data():
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

        cache = get_cache(key=key, query=get_data, timeout=1, cache=Cache)
        return Response(data={"data": cache}, status=200)
    except Exception as error:
        return Response(data={"message": str(error)}, status=500)


@utils.timeout()
@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def get_objects_by_field(
    request: HttpRequest,
    model: Model,
    serializer: Serializer,
    field: dict[Model],
    id: int | None = None,
) -> Response:
    try:
        key = list(field.keys())[0]
        value = field[key].objects.get(id=id)
        objects = utils.serialization(
            model=model,
            serializer=serializer,
            **{key: value},
        )
        return Response(data={"data": objects, "total_count": len(objects)}, status=200)
    except Exception as error:
        return Response(data={"message": str(error)}, status=400)


@utils.timeout()
@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def post_object(request: HttpRequest, serializer: Serializer) -> Response:
    try:
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"data": serializer.data}, status=201)
        return Response(data={"message": serializer.errors}, status=400)
    except Exception as error:
        return Response(data={"message": str(error)}, status=500)


# @utils.timeout()
# @api_view(http_method_names=["POST"])
# @permission_classes([AllowAny])
@csrf_exempt
def post_contract(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            author = (
                request.user
                if request.user.is_authenticated
                else User.objects.get(username="Anonymous")
            )
            # agent = models.Agent.objects.get(bin=request.POST.get("bin", None))
            agent = models.Agent.objects.all().first()
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
            return JsonResponse(
                data={
                    "data": serializers.ContractSerializer(contract, many=False).data
                },
                status=201,
            )
        except Exception as error:
            return JsonResponse(data={"message": str(error)}, status=400)
    return JsonResponse(data={"message": "Method not allowed"}, status=405)
