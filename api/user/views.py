from rest_framework import viewsets, generics, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import ValidationError
from user.serializers import  UserSignInSerializer
from django.contrib.auth import get_user_model 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.settings import api_settings

class UserViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = UserSignInSerializer(instance)
        return Response(serializer.data)
    
    @swagger_auto_schema(
    operation_summary='change your account',
    request_body=UserSignInSerializer
    )
    def update(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = UserSignInSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @swagger_auto_schema(
    operation_summary='create your account',
    request_body=UserSignInSerializer,
    security=[],
    )    
    def create(self, request, *args, **kwargs):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
