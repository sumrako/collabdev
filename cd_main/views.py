from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import datetime
from django.forms import model_to_dict
from .serializers import *
# Create your views here.

class ProjectAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all().filter(soft_delete__in=[False])
        return Response({'Projects':ProjectSerializer(projects, many=True).data})

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Project': serializer.data})

class ProjectTypeAPIView(APIView):
    def get(self, request):
        types = ProjectTypes.objects.all()
        return Response({'ProjectTypes' :ProjectTypesSerializer(types, many=True).data})

class ProjectSkillAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        return Response({'ProjectSkills' : SkillsSerializer(skills, many=True).data})
