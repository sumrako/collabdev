from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *



class ProjectSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    project_type = serializers.PrimaryKeyRelatedField(queryset=ProjectTypes.objects.all())
    class Meta:
        model = Project
        fields = ("title", "description", "skills", "created_at", "update_at", "soft_delete", "project_type")

class SkillsSerializer(serializers.ModelSerializer):
    skills = ProjectSerializer(many=True,read_only=True)
    class Meta:
        model = Skill
        fields = ("skills", "title")

class ProjectTypesSerializer(serializers.ModelSerializer):
    types = ProjectSerializer(read_only=True)
    class Meta:
        model = ProjectTypes
        fields = '__all__'
        depth = 1