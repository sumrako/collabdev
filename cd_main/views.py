from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
import datetime
from django.forms import model_to_dict
# Create your views here.

class ProjectAPIView(APIView):
    def get(self, request):
        lst = Project.objects.all().values()
        return Response({'Projects':list(lst)})
    
    def post(self, request):
        project_new = Project.objects.create(
            title = request.data['title'],
            description = request.data['description'],
            created_at = request.data['created_at'],
            project_type_id = request.data['project_type_id']
        )
        return Response({'Project': model_to_dict(project_new)})
class ProjectTypeAPIView(APIView):
    def get(self, request):
        return Response({'value' :' Рекрутинговый портал'})
class ProjectSkillAPIView(APIView):
    def get(self, request):
        return Response({'valuse' :'Django REST Framework'})