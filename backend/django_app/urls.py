from django.urls import path
from django_app import views, models, serializers

urlpatterns = [
    path("api/", views.api),
    path('api/contracts/', views.objects, {'model': models.Contract, 'serializer': serializers.ContractSerializer}),
    path('api/contract/<int:id>/', views.objects, {'model': models.Contract, 'serializer': serializers.ContractSerializer}),
    path('api/agents/', views.objects, {'model': models.Agent, 'serializer': serializers.AgentSerializer}),
    path('api/agent/<int:id>/', views.objects, {'model': models.Agent, 'serializer': serializers.AgentSerializer}),
    path('api/comments/', views.objects, {'model': models.Comment, 'serializer': serializers.CommentSerializer}),
    path('api/comment/<int:id>/', views.objects, {'model': models.Comment, 'serializer': serializers.CommentSerializer}),
]