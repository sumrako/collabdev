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


class NotificationAPIView(generics.ListAPIView):
    """ API-ручка к оповещениям (запросам на присоединение к проекту)
        в ответ на запрос отвечающий следующей спецификации:

            GET '/notifications' HTTP/1.1
            Query:
                notification_ids: list[int], Optional - filter
                request_user_ids: list[int], Optional - filter
                response_user_ids: list[int], Optional - filter
                project_ids: list[int], Optional - filter
                notification_status_ids: list[int], Optional - filter
                key_words: str, Optional - filter

                order_by: str = 'datetime desc'
                limit: int, Optional, default 10, max 10000
                offset: int, Optional, default 0

            Response json utf-8 {
                [
                    {
                        id: int
                        text: str
                    request_user_id: int
                        response_user_id: int
                        created_at: datetime
                    notification_status_id: int
                    },...
                ]
            }
            Пример: https://collabdev.ru/notifications/?notifications_ids=2&notifications_ids=3&notification_status_ids=2
        Ответ: объекты Notification отвечающие параметрам запросов
    """
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.all()

        key_words = self.request.query_params.get('key_words')
        if key_words is not None:
            for key_word in key_words:
                queryset = queryset.filter(text__contains=key_word)

        notification_ids = self.request.query_params.getlist('notification_ids')
        if notification_ids:
            queryset = queryset.filter(id__in=list(map(int, notification_ids)))

        request_user_ids = self.request.query_params.getlist('request_user_ids')
        if request_user_ids:
            queryset = queryset.filter(request_user__id__in=list(map(int, request_user_ids)))

        response_user_ids = self.request.query_params.getlist('response_user_ids')
        if response_user_ids:
            queryset = queryset.filter(response_user__id__in=list(map(int, response_user_ids)))

        project_ids = self.request.query_params.getlist('project_ids')
        if project_ids:
            queryset = queryset.filter(project__id__in=list(map(int, project_ids)))

        status_ids = self.request.query_params.getlist('notification_status_ids')
        if status_ids:
            queryset = queryset.filter(notification_status__id__in=list(map(int, status_ids)))

        limit = self.request.query_params.get('limit')
        limit = 10 if limit is None else int(limit)

        offset = int(self.request.query_params.get('offset'))
        offset = 0 if offset is None else int(offset)

        order_by = self.request.query_params.get('order_by')
        field, order = order_by.split(',')
        desk_ask = 1 if order == 'ask' else -1

        return queryset.filter.order_by(field)[offset: offset + limit: desk_ask]


class UserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.all()

        fullname = self.request.query_params.get('username')
        if fullname is not None:
            queryset = queryset.filter(username_iexact=fullname)

        users_ids = self.request.query_params.getlist('users_ids')
        if users_ids:
            queryset = queryset.filter(id__in=list(map(int, users_ids)))

        skills_ids = self.request.query_params.getlist('skills_ids')
        if skills_ids:
            queryset = queryset.filter(skills__id__in=skills_ids)

        limit = self.request.query_params.get('limit')
        limit = 10 if limit is None else int(limit)

        offset = int(self.request.query_params.get('offset'))
        offset = 0 if offset is None else int(offset)

        order_by = self.request.query_params.get('order_by')
        field, order = order_by.split(',')
        desk_ask = 1 if order == 'ask' else -1

        return queryset.filter(is_active__in=[True]).order_by(field)[offset: offset + limit: desk_ask]


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


class ProjectOneAPIView(generics.RetrieveUpdateDestroyAPIView):
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

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectTypeAPIView(generics.ListAPIView):
    queryset = ProjectTypes.objects.all()
    serializer_class = ProjectTypesSerializer


class ProjectSkillAPIView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillsSerializer
