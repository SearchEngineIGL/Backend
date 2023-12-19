from rest_framework import serializers
from .models import *
from .managers import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('id','username','email','password')
        extra_kwargs={'password':{'write_only':True}}
    def create(self,validated_data):
        user=CustomUser.objects.create_user(email=validated_data['email'],username=validated_data['username'],password=validated_data['password'],user_type="simple")
        return user
        
        
# class AdminUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=AdminUser
#         fields=('id','username','email','password')
#         extra_kwargs={'password':{'write_only':True}}
#     def create(self,username,email,password):
#         adminUser=AdminUser.objects.create_user(username,email,password)
#         return adminUser
        
        
# class ModeratorUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=ModeratorUser
#         fields=('id','username','email','password')
#         extra_kwargs={'password':{'write_only':True}}
#     def create(self,username,email,password):
#         moderatorUser=ModeratorUser.objects.create_user(username,email,password)
#         return moderatorUser
    
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.CharField(max_length=255)
    password=serializers.CharField(max_length=255,write_only=True)
    access_token=serializers.CharField(max_length=255,read_only=True)
    refresh_token=serializers.CharField(max_length=255,read_only=True)
    class Meta:
        model=CustomUser
        fields=['email','password','access_token','refresh_token','user_type']
    def validate(self,attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        request=self.context.get('request')
        user = CustomUser.objects.authenticate_user(email=email, password=password)
        if not user:
            raise AuthenticationFailed("invalid credentials try again")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")
        user_tokens=user.tokens()
        
        return{
            'email':user.email,
            'access_token':str(user_tokens.get('access')),
            'refresh_token':str(user_tokens.get('refresh')),
        }
            
        
                