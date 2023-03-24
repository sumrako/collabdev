from rest_framework import serializers

from .models import Project, Skill, ProjectTypes
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())])
#
#     password1 = serializers.CharField(
#         write_only=True, required=True, validators=[validate_password])
#
#     password2 = serializers.CharField(write_only=True, required=True)
#     birth_date = serializers.DateField(required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', 'birth_date', 'email', 'first_name', 'last_name')
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': True},
#         }
#
#     def validate(self, attrs):
#         if attrs['password1'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {'password1': "password field dont match !"})
#
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#         )
#
#         user.set_password(validated_data['password1'])
#         custom_user = CustomUser.objects.create(user=user, birth_date=validated_data['birth_date'])
#
#         custom_user.save()
#         user.save()
#
#         return custom_user


# class UserSerializer(serializers.ModelSerializer):
#     projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True)
#     skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = User
#         fields = ("id", "skills", "projects", "birth_date", "user_avatar")


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
