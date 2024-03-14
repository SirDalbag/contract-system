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
    author = serializers.SerializerMethodField()
    agent = serializers.SerializerMethodField()
    # comment = serializers.SerializerMethodField()

    class Meta:
        model = models.Contract
        exclude = ["agent_id"]  # "comment_id"

    @staticmethod
    def get_author(contract):
        try:
            author = contract.author.username
            return author
        except Exception as error:
            return str(error)

    @staticmethod
    def get_agent(contract):
        try:
            agent = contract.agent_id.bin
            return agent
        except Exception as error:
            return str(error)

    # @staticmethod
    # def get_comment(contract):
    #     try:
    #         comment = contract.comment_id.comment
    #         return comment
    #     except Exception as error:
    #         return str(error)


class PostContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contract
        exclude = ["date"]
