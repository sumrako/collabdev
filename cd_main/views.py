from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status


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
                "jwt": {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
        })


class UserAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


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
