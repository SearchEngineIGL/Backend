from rest_framework import serializers
from .models import *
from .managers import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str,smart_bytes,force_str
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken,Token
from rest_framework_simplejwt.exceptions import TokenError

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('id','username','email','password')
        extra_kwargs={'password':{'write_only':True}}
        
    def create(self,validated_data):
        user=CustomUser.objects.create_user(email=validated_data['email'],username=validated_data['username'],password=validated_data['password'],user_type="simple")
        return user
        
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('id','username','email')
        
        
 
    
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
        if not user.is_verified and user.user_type=='simple':
            raise AuthenticationFailed("Email is not verified")
        user_tokens=user.tokens()
        
        return{
            'email':user.email,
            'user_type':user.user_type,
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
            site_domain="http://localhost:5173"
            print('ablaaa')
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            abslink=f"http://{site_domain}{relative_link}"
            
            email_body=f"Salam Alaikoum, \n use the link below to reset your password : \n{abslink}"
            data={
                'email_body':email_body,
                'email_subject':"Reset your Password",
                'to_email':user.email
            }
            send_normal_email(data)
        return super().validate(attrs)
        

class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100,min_length=6,write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)

    class Meta:
        fields=["password","uidb64","token"]
    def validate(self,attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed("reset link is invalid or has expired")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed("Link is invalid or has expired !")
                
class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()
    
    default_error_messages={
        'bad_token':('Token is invalid or has expired')
    }
    
    def validate(self,attrs):
        self.token=attrs.get('refresh_token')
        return attrs
    
    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')