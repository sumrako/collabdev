from django.shortcuts import render
from rest_framework import generics
from .models import *
import datetime
from django.forms import model_to_dict
from .serializers import *
from django.shortcuts import get_object_or_404
# Create your views here.

class ProjectAPIView(generics.ListAPIView, generics.ListCreateAPIView):
    queryset = Project.objects.all().filter(soft_delete__in=[False]) 
    serializer_class = ProjectSerializer
    def perform_create(self,serializer):
        serializer.save()

class ProjectOneAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Project.objects.all().filter(soft_delete__in=[False])
    serializer_class = ProjectSerializer
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class ProjectTypeAPIView(generics.ListAPIView):
    queryset = ProjectTypes.objects.all()
    serializer_class = ProjectTypesSerializer

class ProjectSkillAPIView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillsSerializer
