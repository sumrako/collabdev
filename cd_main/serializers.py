from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *

class ProjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=5000)
    skills = serializers.ListField()
    created_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)
    soft_delete = serializers.BooleanField()
    
    def create(self, validated_data):
        return Project.objects.create(**validated_data)