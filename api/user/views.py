from rest_framework import viewsets, views, generics, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.settings import api_settings
from user.serializers import  UserSerializer, RegisterSerializer, \
     RequestPasswordResetSerializer, SetNewPasswordSerializer
from django.contrib.auth import get_user_model 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api import settings 
import jwt


class UserViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='讀取個人帳號資料',
    )     
    def retrieve(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = UserSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary='修改帳號資料',
        request_body=UserSerializer
    )
    def update(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = UserSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_summary='註冊帳號',
        operation_description='password_check應輸入和password一樣的值，確認使用者沒有打錯密碼。 \
            隨後寄出確認信，十分鐘內點擊信件中的url，即可啟動帳號。',
        request_body=RegisterSerializer,
        security=[]
    )  
    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': 'We have sent you a link to verify your email, \
            please finish it wihtin 3 hours.'}, status=status.HTTP_201_CREATED)


class VerifyEmailView(views.APIView):
    # serializer_class is for swagger, didn't work in the verification

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(
        operation_summary='驗證信箱啟動帳號',
        operation_description='確認信中的url會以GET, main domain/?token={jwt token} 的方式驗證信箱，並啟動帳號。',
        manual_parameters=[token_param_config],        
        security=[])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = get_user_model().objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)            


class RequestPasswordResetView(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer

    @swagger_auto_schema(
        operation_summary='請求重設密碼',
        operation_description='確認帳號和以及對應信箱後，寄出能修改密碼的網址。用戶可在十分鐘內來到該網址修改密碼，十分鐘後該網址作廢。',
        security=[])    
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': 'We have sent you a link to reset your password, \
            please finish it wihtin 10 minutes.'}, status=status.HTTP_200_OK)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    @swagger_auto_schema(
        operation_summary='重設密碼網址',
        operation_description='該網址會在用戶請求重設密碼後寄出，用戶可在十分鐘內來到該網址修改密碼，十分鐘後該網址作廢。',
        security=[])    
    def patch(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        instance = get_user_model().objects.get(id=payload['user_id'])
        if instance.is_active != False:
            return Response({'error': 'Password is not reset yet'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SetNewPasswordSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
