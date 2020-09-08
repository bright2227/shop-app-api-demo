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

    @swagger_auto_schema(
    operation_summary='讀取帳號資料',
    operation_description='password為hash後的帳號密碼。',
    )     
    def retrieve(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = UserSignInSerializer(instance)
        return Response(serializer.data)
    
    @swagger_auto_schema(
    operation_summary='修改帳號資料',
    operation_description='password_check應輸入帳號原本的密碼以做確認，password為修改後的密碼。',
    request_body=UserSignInSerializer
    )
    def update(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = UserSignInSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @swagger_auto_schema(
    operation_summary='註冊帳號',
    operation_description='password_check應輸入和password一樣的值，確認使用者沒有打錯密碼。',
    request_body=UserSignInSerializer,
    security=[]
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
