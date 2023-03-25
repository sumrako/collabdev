from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        id_ = dict(response.data)['id']
        user = CustomUser.objects.get(id=id_)
        refresh = RefreshToken.for_user(user)
        return Response({
                'user': response.data,
                "jwt": {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
        })


class UserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = CustomUser.objects.all()

        fullname = self.request.query_params.get('username')
        if fullname is not None:
            queryset = queryset.filter(username_iexact=fullname)

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

        return queryset.filter(is_active=True).order_by(field)[offset: offset + limit: desk_ask]


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
