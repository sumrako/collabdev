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
        projects = Project.objects.all()
        return Response({'Projects':ProjectSerializer(projects, many=True).data})
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Project': serializer.data})
    
class ProjectTypeAPIView(APIView):
    def get(self, request):
        return Response({'value' :' Рекрутинговый портал'})
class ProjectSkillAPIView(APIView):
    def get(self, request):
        return Response({'valuse' :'Django REST Framework'})