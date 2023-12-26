from rest_framework import serializers
from .models import *
from authenticationApp.managers import *
from authenticationApp.serializers import *


class CreateModeratorserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('id','username','email','password')
        extra_kwargs={'password':{'write_only':True}}
    def create(self,validated_data):
        user=CustomUser.objects.create_moderator_user(email=validated_data['email'],username=validated_data['username'],password=validated_data['password'],user_type="moderator")
        return user
        
      
