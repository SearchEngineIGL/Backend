from rest_framework import serializers
from .models import *

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=SimpleUser
        fields=('id','username','email','password')
        extra_kwargs={'password':{'write_only':True}}
    def create(self,validated_data):
        simpleUser=SimpleUser.objects.create_user(**validated_data)
        return simpleUser
        

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminUser
        fields=('id','username','email','password')
        extra_kwargs={'password':{'write_only':True}}
    def create(self,username,email,password):
        adminUser=AdminUser.objects.create_user(username,email,password)
        return adminUser
        
        
class ModeratorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=ModeratorUser
        fields=('id','username','email','password')
        extra_kwargs={'password':{'write_only':True}}
    def create(self,username,email,password):
        moderatorUser=ModeratorUser.objects.create_user(username,email,password)
        return moderatorUser
                