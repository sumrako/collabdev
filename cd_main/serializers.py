from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True)
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)

    class Meta:
        model = User
        fields = ("id", "fullname", "skills", "projects", "birth_date", "user_avatar")


class ProjectSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    project_type = serializers.PrimaryKeyRelatedField(queryset=ProjectTypes.objects.all())

    class Meta:
        model = Project
        fields = ("title", "description", "skills", "created_at", "updated_at", "soft_delete", "project_type")


class SkillsSerializer(serializers.ModelSerializer):
    skills = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Skill
        fields = ("skills", "title")


class ProjectTypesSerializer(serializers.ModelSerializer):
    types = ProjectSerializer(read_only=True)

    class Meta:
        model = ProjectTypes
        fields = '__all__'
        depth = 1
