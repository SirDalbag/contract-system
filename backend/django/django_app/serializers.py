from rest_framework import serializers
from django.contrib.auth.models import User
from django_app import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Agent
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    agent = serializers.SerializerMethodField()

    class Meta:
        model = models.Contract
        fields = "__all__"

    @staticmethod
    def get_username(contract):
        try:
            username = contract.author.username
            return username
        except Exception as error:
            return str(error)

    @staticmethod
    def get_agent(contract):
        try:
            agent = contract.agent_id.bin
            return agent
        except Exception as error:
            return str(error)


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Log
        fields = "__all__"
