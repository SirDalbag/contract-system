from django.urls import path
from django_app import views, models, serializers

urlpatterns = [
    path("api/", views.api),
    path('api/get/contracts/', views.get_objects_or_object, {'model': models.Contract, 'serializer': serializers.ContractSerializer}),
    path('api/get/contract/<int:id>/', views.get_objects_or_object, {'model': models.Contract, 'serializer': serializers.ContractSerializer}),
    path('api/post/contract/', views.post_object, {'serializer': serializers.ContractSerializer}),
    path('api/get/agents/', views.get_objects_or_object, {'model': models.Agent, 'serializer': serializers.AgentSerializer}),
    path('api/get/agent/<int:id>/', views.get_objects_or_object, {'model': models.Agent, 'serializer': serializers.AgentSerializer}),
    path('api/post/agent/', views.post_object, {'serializer': serializers.AgentSerializer}),
    path('api/get/comments/', views.get_objects_or_object, {'model': models.Comment, 'serializer': serializers.CommentSerializer}),
    path('api/get/comment/<int:id>/', views.get_objects_or_object, {'model': models.Comment, 'serializer': serializers.CommentSerializer}),
    path('api/post/comment/', views.post_object, {'serializer': serializers.CommentSerializer}),
    path('api/get/contracts/author/<int:id>', views.get_contracts_by_author),
]