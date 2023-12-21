from rest_framework import serializers
from .models import *
from .managers import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str,smart_bytes
from django.urls import reverse
from .utils import send_normal_email

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
            
            
class PasswordResetRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta :
        fields=['email']
    def validate(self,attrs):
        email=attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user=CustomUser.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))# we try to code user id into string tha we can read
            token=PasswordResetTokenGenerator().make_token(user)
            request =self.context.get('request')
            site_domain=get_current_site(request).domain
            relative_link=reverse('password-reset-confirm',kwargs=[{'uidb64':uidb64, 'token':token}])
            abslink=f"http://{site_domain}{relative_link}"
            email_body=f"Salam Alaikoum, \n use the link below to reset your password : \n{abslink}"
            data={
                'email_body':email_body,
                'email_subject':"Reset your Password",
                'to_email':user.email
            }
            send_normal_email(data)
        return super().validate(attrs)
        
                