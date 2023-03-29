from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics, status


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        id_ = dict(response.data)['id']
        user = CustomUser.objects.get(id=id_)
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': response.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)


class SingleUserView(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            refresh = RefreshToken(refresh_token)
            token = refresh.access_token
            user = CustomUser.objects.get(id=refresh.payload['user_id'])
            serializer = UserSerializer(user)
            return Response({'user': serializer.data, 'access': str(token), 'refresh': str(refresh)},
                            status=status.HTTP_200_OK)
        except (CustomUser.DoesNotExist, TypeError, ValueError):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

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


class UserDetailsView(generics.ListAPIView):
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        queryset = CustomUser.objects.filter(username=username)
        return queryset


class ProjectAPIView(generics.ListAPIView, generics.ListCreateAPIView):
    queryset = Project.objects.all().filter(soft_delete__in=[False])
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        self.check_permissions(self.request)
        project = serializer.save()
        user_project_relation_serializer = UserProjectRelationSerializer(
            data={'user': self.request.user.id, 'project': project.id})
        if user_project_relation_serializer.is_valid():
            user_project_relation_serializer.save()


class ProjectOneAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Project.objects.all().filter(soft_delete__in=[False])
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        self.check_permissions(self.request)
        project_id = kwargs.get('id')
        user_projects = UserSerializer(request.user).data.get('projects')
        if project_id in user_projects:
            return self.update(request, *args, **kwargs)
        else:
            return Response({'message': 'Project ID is not in user projects'}, status=status.HTTP_400_BAD_REQUEST)


class ProjectTypeAPIView(generics.ListAPIView):
    queryset = ProjectTypes.objects.all()
    serializer_class = ProjectTypesSerializer


class ProjectSkillAPIView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillsSerializer
