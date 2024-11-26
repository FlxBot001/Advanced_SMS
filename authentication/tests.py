from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import serializers


# Serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            user_id = validated_data['user_id'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Views

class RegisterView(APIView):
    """
    Handle user registration (sign-up)
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # Serialize the user to return the response
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    This view is an override of the TokenObtainPairView to allow custom responses if needed
    """
    pass  # You can override methods like post here to customize the response if needed


class CustomTokenRefreshView(TokenRefreshView):
    """
    This view is an override of the TokenRefreshView to allow custom responses if needed
    """
    pass  # You can override methods like post here to customize the response if needed
