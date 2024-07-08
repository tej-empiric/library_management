from rest_framework.response import Response
from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework import status, viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework import views
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            refreshToken = RefreshToken(refresh_token)
            refreshToken.blacklist()

            return Response(
                {"Log out successfull."}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {f"Error in Log out. {str(e)}, {status.HTTP_400_BAD_REQUEST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class StaffView(generics.ListAPIView):
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser == True:
            return CustomUser.objects.filter(role="staff")
        else:
            raise PermissionDenied("You do not have permission to perform this action.")


class StaffUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role="staff")
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(email=self.request.user)
