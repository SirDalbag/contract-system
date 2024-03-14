from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_app import models, serializers, utils
from django.views.decorators.csrf import csrf_exempt


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
def post_object_super_slozno_no_kruto(request, serializer):
    try:
        serializer = serializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    except Exception as error:
        return Response(data={"message": str(error)})


@csrf_exempt
def post_object(request):
    try:
        print(request.POST)
        print(request.FILES)
        date = request.POST.get("date", None)
        total = request.POST.get("total", None)
        comment = request.POST.get("comment", None)
        file = request.FILES.get("file_path", None)
        agent_title = request.POST.get("agent_title", None)
        comment_obj = models.Comment.objects.create(comment=comment)
        agent_id = models.Agent.objects.get(title=agent_title)
        contract = models.Contract.objects.create(
            author=request.user,
            agent_id=agent_id,
            comment_id=comment_obj,
            total=total,
            date=date,
            file_path=file,
        )
        print(contract)
        return JsonResponse(
            data={"data": serializers.ContractSerializers(comment_obj, many=False).data}
        )
    except Exception as error:
        print(error)
        return JsonResponse(data={"message": str(error)})


# <QueryDict: {'comment': ['hgh'], 'total': ['10'], 'contract': [''], 'date': ['2024-03-14']}>
# <MultiValueDict: {'file_path': [<InMemoryUploadedFile: contract_O3dO5f8_WYq5pQD.pdf (application/pdf)>]}>


@csrf_exempt
def post(request):
    print(request.POST)
    print(request.FILES)
    return JsonResponse({"message": "OK"})
