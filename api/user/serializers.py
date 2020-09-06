from rest_framework import serializers
from django.contrib.auth import get_user_model 


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
        user = get_user_model()(**validated_data)  # it is instance, don't trigger the sql
        user.set_password(validated_data['password'])
        user.save()
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
