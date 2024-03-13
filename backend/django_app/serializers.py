from rest_framework import serializers
from django_app import models

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Agent
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contract
        fields = "__all__"