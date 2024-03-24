from django.urls import path
from django_app import views, models, serializers
from django.contrib.auth.models import User
from django_app.swagger import schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("", views.index),
    path("api/", views.api),
    path(
        "api/contracts/",
        views.get_objects_or_object,
        {
            "model": models.Contract,
            "serializer": serializers.ContractSerializer,
            "key": "contracts",
        },
    ),
    path(
        "api/contracts/<int:id>/",
        views.get_objects_or_object,
        {
            "model": models.Contract,
            "serializer": serializers.ContractSerializer,
            "key": "contract",
        },
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
        {
            "model": models.Agent,
            "serializer": serializers.AgentSerializer,
            "key": "agents",
        },
    ),
    path(
        "api/agents/<int:id>/",
        views.get_objects_or_object,
        {
            "model": models.Agent,
            "serializer": serializers.AgentSerializer,
            "key": "agent",
        },
    ),
    path(
        "api/agent/",
        views.post_object,
        {"serializer": serializers.AgentSerializer},
    ),
    path(
        "api/comments/",
        views.get_objects_or_object,
        {
            "model": models.Comment,
            "serializer": serializers.CommentSerializer,
            "key": "comments",
        },
    ),
    path(
        "api/comments/<int:id>/",
        views.get_objects_or_object,
        {
            "model": models.Comment,
            "serializer": serializers.CommentSerializer,
            "key": "comment",
        },
    ),
    path(
        "api/comment/",
        views.post_object,
        {"serializer": serializers.CommentSerializer},
    ),
    path(
        "api/logs/",
        views.get_objects_or_object,
        {"model": models.Log, "serializer": serializers.LogSerializer, "key": "logs"},
    ),
    path(
        "api/logs/<int:id>",
        views.get_objects_or_object,
        {"model": models.Log, "serializer": serializers.LogSerializer, "key": "log"},
    ),
    path("api/user/register/", views.register),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/token/verify/", TokenVerifyView.as_view()),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
