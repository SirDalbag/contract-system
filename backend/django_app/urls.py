from django.urls import path
from django_app import views, models, serializers
from django.contrib.auth.models import User

urlpatterns = [
    path("api/", views.api),
    path(
        "api/get/contracts/",
        views.get_objects_or_object,
        {"model": models.Contract, "serializer": serializers.ContractSerializer},
    ),
    path(
        "api/get/contracts/<int:id>/",
        views.get_objects_or_object,
        {"model": models.Contract, "serializer": serializers.ContractSerializer},
    ),
    path(
        "api/get/contracts/author/<int:id>",
        views.get_objects_by_field,
        {
            "model": models.Contract,
            "serializer": serializers.ContractSerializer,
            "field": {"author": User},
        },
    ),
    path(
        "api/get/contracts/agent/<int:id>",
        views.get_objects_by_field,
        {
            "model": models.Contract,
            "serializer": serializers.ContractSerializer,
            "field": {"agent_id": models.Agent},
        },
    ),
    path(
        "api/post/contract/",
        views.post_object,
        {"serializer": serializers.PostContractSerializer},
    ),
    path(
        "api/get/agents/",
        views.get_objects_or_object,
        {"model": models.Agent, "serializer": serializers.AgentSerializer},
    ),
    path(
        "api/get/agents/<int:id>/",
        views.get_objects_or_object,
        {"model": models.Agent, "serializer": serializers.AgentSerializer},
    ),
    path(
        "api/post/agent/",
        views.post_object,
        {"serializer": serializers.AgentSerializer},
    ),
    path(
        "api/get/comments/",
        views.get_objects_or_object,
        {"model": models.Comment, "serializer": serializers.CommentSerializer},
    ),
    path(
        "api/get/comments/<int:id>/",
        views.get_objects_or_object,
        {"model": models.Comment, "serializer": serializers.CommentSerializer},
    ),
    path(
        "api/post/comment/",
        views.post_object,
        {"serializer": serializers.CommentSerializer},
    ),
]
