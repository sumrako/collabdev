from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *
import io
class ProjectModel:
    def __init__(self, title, description):
        self.title = title
        self.description = description

class ProjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=5000)
    #created_at = models.DateTimeField(auto_now_add=True)
    #update_at = models.DateTimeField(auto_now=True)
    #soft_delete = models.BooleanField(default=False)

class Meta:
    model = Project
    fields = ('title', 'description')

def encode():
    model = ProjectModel('title: BuySell1', 'description: Redan MOSH')
    #'created_at':'02.03.20231',
    #'project_type_id':41
    model_sr = ProjectSerializer(model)
    json = JSONRenderer().render(model_sr.data)
    print(json)

def decode():
    stream = io.BytesIO(b'{"title":"title: BuySell1","description":"description: \xd0\xa0\xd0\x95\xd0\x94\xd0\x90\xd0\x9d \xd0\xa1\xd0\x98\xd0\x9b\xd0\x901"}')
    data = JSONParser().parse(stream)