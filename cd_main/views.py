from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *


# Create your views here.
class UserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_class = []
    def get_queryset(self):
        queryset = User.objects.all()

        fullname = self.request.query_params.get('fullname')
        if fullname is not None:
            queryset = queryset.filter(fullname__iexact=fullname)

        users_ids = self.request.query_params.get('user_ids')
        if users_ids is not None:
            queryset = queryset.filter(id__in=users_ids)

        skills_ids = self.request.query_params.get('skills_ids')
        if skills_ids is not None:
            queryset = queryset.filter(skills__in=skills_ids)

        limit = self.request.query_params.get('limit')
        offset = self.request.query_params.get('offset')
        order_by = self.request.query_params.get('order_by')
        field, order = order_by.split()
        desk_ask = 1 if order == 'ask' else -1

        return queryset.order_by(field)[offset: offset + limit: desk_ask]


class ProjectAPIView(generics.ListAPIView, generics.ListCreateAPIView):
    queryset = Project.objects.all().filter(soft_delete__in=[False])
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save()


class ProjectTypeAPIView(generics.ListAPIView):
    queryset = ProjectTypes.objects.all()
    serializer_class = ProjectTypesSerializer


class ProjectSkillAPIView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillsSerializer
