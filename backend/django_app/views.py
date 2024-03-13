from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_app import utils

@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def api(request):
    return Response(data={"message": "OK"})

@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def objects(request, model, serializer, id: int = None):
    return Response(data={"message": utils.serialization(model, serializer, id=id) if id else utils.serialization(model, serializer, sort=request.GET.get("sort", None))})