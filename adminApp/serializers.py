from rest_framework import serializers
from .models import *
from authenticationApp.managers import *
from authenticationApp.serializers import *


class CreateModeratorserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('id','username','email')
        extra_kwargs={'password':{'write_only':True}}
    def create(self,validated_data):
        user=CustomUser.objects.create_moderator_user(email=validated_data['email'],username=validated_data['username'],user_type="moderator")
        return user
        
class ModifyAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.get('password', instance.password)

        # Update other fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # Set the password using the set_password method for proper hashing
        instance.set_password(password)

        instance.save()
        return instance