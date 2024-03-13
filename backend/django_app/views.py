from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_app import models, serializers, utils

@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def api(request):
    if request.method == "GET":
        return Response(data={"message": "OK"})
    elif request.method == "POST":
        return Response(data={"message": request.data})

@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def get_objects_or_object(request, model, serializer, id: int = None):
    return Response(data={"data": utils.serialization(model, serializer, id=id) if id else utils.serialization(model, serializer, sort=request.GET.get("sort", None))})

@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def post_object(request, serializer):
    serializer = serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def get_contracts_by_author(request, id: int = None):
    try:
        author = User.objects.get(id=id)
        contracts = models.Contract.objects.filter(author=author)
        serializer = serializers.ContractSerializer(contracts, many=True)
        total_count = contracts.count()
        return Response(data={"data": serializer.data, "total_count": total_count})
    except Exception as error:
        return Response(data={"data": "", "total_count": 0, "message": str(error)}, status=400)