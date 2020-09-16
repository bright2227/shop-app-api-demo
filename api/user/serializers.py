from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model 
from django.contrib.sites.shortcuts import get_current_site
from core.models import Order
# from user.tasks import send_verified_mail_task
from django.core.mail import send_mail
from django.shortcuts import render, reverse
import datetime


class UserSignInSerializer(serializers.ModelSerializer):
    # you habe to use CharField(write_only=True) Only appying write_only_fields 
    # not works perfectly. something went wrong in to_representaion part
    password_check = serializers.CharField(write_only=True) 

    def validate_password_check(self, attr):
        if attr != self.initial_data['password']:
            raise serializers.ValidationError("Your double password check fails") 
        return attr

    def create(self, validated_data):
#         User() = get_user_model()
        validated_data.pop('password_check')
        # it is instance, doesn't trigger the sql
        user = get_user_model()(**validated_data)  
        user.set_password(validated_data['password'])
        user.save()
        # create a order for cart
        Order.objects.create(user=user, state='CR')
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('password_check')
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

    class Meta:
        model =  get_user_model()
        fields  = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'password_check')
        write_only_fields = ('password', 'password_check')
        read_only_fields = ('id',)
        extra_kwargs = {'email': {'read_only': False, 'required': True}}


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

        RefreshToken.lifetime= datetime.timedelta(minutes=200)
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(self.context['request']).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token="+str(token)
        email_body = 'Hi ' + user.username + \
            ' Use the link below to active your account and verify your email \n' + absurl
 
        send_mail('Verification mail from shop api',
            email_body,
            'bright2227@gmail.com',
            [validated_data['email']])
        return user

    class Meta:
        model =  get_user_model()
        fields  = ('username', 'password', 'email', 'first_name', 'last_name', 'password_check')
        write_only_fields = ('password', 'password_check')
