from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model 
from django.contrib.sites.shortcuts import get_current_site
from core.models import Order
from user.tasks import send_mail_verify, send_mail_passreset
from django.shortcuts import render, reverse
import datetime
from django.core.mail import send_mail
from django.core.cache import cache 
import secrets


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=68, min_length=4, 
        required=True,
    )  
    class Meta:
        model =  get_user_model()
        fields  = ('username', 'email', 'first_name', 'last_name',)
        read_only_fields = ('email',)


class RegisterSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        max_length=68, min_length=6, 
        write_only=True,
        required=True,
    )
    username = serializers.CharField(
        max_length=68, min_length=4, 
        write_only=True,
        required=True,
    )

    def validate_password_check(self, attr):
        if attr != self.initial_data['password']:
            raise serializers.ValidationError("Your password double check fails") 
        return attr

    def create(self, validated_data):
        validated_data.pop('password_check')
        # it is instance, doesn't trigger the sql
        user = get_user_model()(**validated_data)  
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        # create a order for cart
        Order.objects.create(user=user, state='CR')
        # create a jwt token
        RefreshToken.lifetime= datetime.timedelta(minutes=200)
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(self.context['request']).domain
        relativeLink = reverse('email-verify')
        # absurl = 'http://' + current_site + relativeLink + "?token="+str(token)
        absurl = 'http://'  + current_site + '/register?token='+str(token)  #for local frontend test
        email_body = 'Hi ' + user.username + \
            ' Use the link below to active your account and verify your email \n' + absurl

        send_mail_verify.delay(email_body, validated_data['email'])
        # send_mail('Verification mail from shop api',
        #     email_body,
        #     'bright2227@gmail.com',
        #     [validated_data['email']])
        return user

    class Meta:
        model =  get_user_model()
        fields  = ('username', 'password', 'email', 'first_name', 'last_name', 'password_check')
        write_only_fields = ('password', 'password_check')


class RequestPasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(
        max_length=68, min_length=4, 
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'username')         

    def create(self, validated_data):
        try:
            user = get_user_model().objects.get(email=validated_data['email'], username=validated_data['username'])
            user.is_active = False
            user.save()
        except:
            raise serializers.ValidationError('email or username is wrong, please check it again')

        # RefreshToken.lifetime = datetime.timedelta(minutes=200)
        # token = RefreshToken.for_user(user).access_token            
        token =  secrets.token_urlsafe(32)
        cache.set(token, user.id, timeout=720)

        current_site = get_current_site(request=self.context['request']).domain
        relativeLink = reverse('passreset-setpass', kwargs={'token': token})
        # absurl = 'http://' + current_site + relativeLink
        absurl = 'http://' + current_site + '/reset/'+str(token)  #for local frontend test

        email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
        
        send_mail_passreset.delay(email_body, validated_data['email'])
        # send_mail('Reset mail from shop api',
        #     email_body,
        #     'bright2227@gmail.com',
        #     [validated_data['email']])         
        return user


class SetNewPasswordSerializer(serializers.ModelSerializer):    
    password = serializers.CharField(
        max_length=68, min_length=6, 
        write_only=True,
        required=True,
    )

    class Meta:
        model = get_user_model()
        fields = ('password', )  

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.is_active = True
        instance.save()
        return instance
