from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render
from django_app import models, serializers, utils


def index(request):
    return render(request, "index.html")


@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def api(request):
    if request.method == "GET":
        return Response(data={"message": "OK"})
    elif request.method == "POST":
        return Response(data={"message": request.data})


@utils.timeout()
@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def get_objects_or_object(request, model, serializer, id=None):
    try:
        return Response(
            data={
                "data": (
                    utils.serialization(model, serializer, id=id)
                    if id
                    else utils.serialization(
                        model,
                        serializer,
                        filter=request.GET.get("filter", None),
                        sort=request.GET.get("sort", None),
                    )
                )
            }
        )
    except Exception as error:
        return Response(data={"message": str(error)})


@utils.timeout()
@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def get_objects_by_field(request, model, serializer, field, id=None):
    try:
        key = list(field.keys())[0]
        value = field[key].objects.get(id=id)
        objects = utils.serialization(
            model,
            serializer,
            **{key: value},
        )
        return Response(data={"data": objects, "total_count": len(objects)})
    except Exception as error:
        return Response(data={"message": str(error)})


@utils.timeout()
@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def post_object(request, serializer):
    try:
        serializer = serializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    except Exception as error:
        return Response(data={"message": str(error)})


@utils.timeout()
@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def post_contract(request):
    try:
        author = request.user
        agent = models.Agent.objects.get(bin=request.POST.get("bin", None))
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
            data={"data": serializers.ContractSerializer(contract, many=False).data}
        )
    except Exception as error:
        return JsonResponse(data={"message": str(error)})
