from rest_framework import serializers, generics
from .models import Project, Skill, ProjectTypes, UserProjectRelation, Notification
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True)
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "skills", "birth_date", "user_avatar", "projects")


class ProjectSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(slug_field='title', queryset=Skill.objects.all(), many=True)
    project_type = serializers.SlugRelatedField(slug_field='title', queryset=ProjectTypes.objects.all())
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = ("id", "users", "title", "description", "skills", "created_at", "updated_at", "soft_delete", "project_type")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(read_only=True, many=True)
    skills = serializers.SlugRelatedField(slug_field='title', queryset=Skill.objects.all(), many=True)

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "skills", "projects", "birth_date", "user_avatar")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        if not user.check_password(password):
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    password2 = serializers.CharField(write_only=True, required=True)
    birth_date = serializers.DateField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password1', 'password2', 'birth_date', 'email', 'first_name', 'last_name', "projects")

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password1': "password field dont match !"})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birth_date=validated_data['birth_date']
        )
        user.set_password(validated_data['password1'])
        user.save()

        return user


class UserProjectRelationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = UserProjectRelation
        fields = ('user', 'project', 'created_at')


class SkillsSerializer(serializers.ModelSerializer):
    skills = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Skill
        fields = '__all__'


class ProjectTypesSerializer(serializers.ModelSerializer):
    types = ProjectSerializer(read_only=True)

    class Meta:
        model = ProjectTypes
        fields = '__all__'
        depth = 1
