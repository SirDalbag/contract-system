from django.urls import path
from django_app import views, models, serializers
from django.contrib.auth.models import User

urlpatterns = [
    path("", views.index),
    path("api/", views.api),
    path(
        "api/contracts/",
        views.get_objects_or_object,
        {"model": models.Contract, "serializer": serializers.ContractSerializer},
    ),
    path(
        "api/contracts/<int:id>/",
        views.get_objects_or_object,
        {"model": models.Contract, "serializer": serializers.ContractSerializer},
    ),
    path(
        "api/contracts/author/<int:id>",
        views.get_objects_by_field,
        {
            "model": models.Contract,
            "serializer": serializers.ContractSerializer,
            "field": {"author": User},
        },
    ),
    path(
        "api/contracts/agent/<int:id>",
        views.get_objects_by_field,
        {
            "model": models.Contract,
            "serializer": serializers.ContractSerializer,
            "field": {"agent_id": models.Agent},
        },
    ),
    path(
        "api/contract/",
        views.post_contract,
    ),
    path(
        "api/agents/",
        views.get_objects_or_object,
        {"model": models.Agent, "serializer": serializers.AgentSerializer},
    ),
    path(
        "api/agents/<int:id>/",
        views.get_objects_or_object,
        {"model": models.Agent, "serializer": serializers.AgentSerializer},
    ),
    path(
        "api/agent/",
        views.post_object,
        {"serializer": serializers.AgentSerializer},
    ),
    path(
        "api/comments/",
        views.get_objects_or_object,
        {"model": models.Comment, "serializer": serializers.CommentSerializer},
    ),
    path(
        "api/comments/<int:id>/",
        views.get_objects_or_object,
        {"model": models.Comment, "serializer": serializers.CommentSerializer},
    ),
    path(
        "api/comment/",
        views.post_object,
        {"serializer": serializers.CommentSerializer},
    ),
    path(
        "api/logs/",
        views.get_objects_or_object,
        {"model": models.Log, "serializer": serializers.LogSerializer},
    ),
    path(
        "api/logs/<int:id>",
        views.get_objects_or_object,
        {"model": models.Log, "serializer": serializers.LogSerializer},
    ),
]
