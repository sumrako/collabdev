from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class ProjectAPIView(APIView):
    def get(self, request):
        return Response({'project_id': '1', 'title': 'Турболыжи', 'description': 'МЫ В РЕДАНЕ', 'type_id': '1', 'created_at': '01.03.2023', 'skills_ids': [1,2,3]})
class ProjectTypeAPIView(APIView):
    def get(self, request):
        return Response({'Рекрутинговый портал'})
class ProjectSkillAPIView(APIView):
    def get(self, request):
        return Response({'Django REST Framework'})