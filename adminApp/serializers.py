from rest_framework import serializers
from .models import *
from authenticationApp.managers import *
from authenticationApp.serializers import *
from .utils import *
from article_processing.elasticsearch_utils import *


"""_summary_
    Class to serialize data of an modeartor object
    Returns:
        _user_: _type of  moderator_
    """
class CreateModeratorserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('id','FullName','username','email','PhoneNumber','photo')
        extra_kwargs={'password':{'write_only':True},
                      'FullName':{'required':False},
                      'PhoneNumber':{'required':False}}
    def create(self,validated_data):
        user=CustomUser.objects.create_moderator_user(email=validated_data['email'],username=validated_data['username'],user_type="moderator")
        if 'FullName' in validated_data:
             user.FullName = validated_data['FullName']
        if 'PhoneNumber' in validated_data:
            user.PhoneNumber = validated_data['PhoneNumber']
        user.save()
        return user
 
"""
Class to serialze the admin object
"""       
class ModifyAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'FullName','username', 'email', 'password','photo')
        extra_kwargs = {'password': {'write_only': True,'required': False},
                        'FullName': {'required': False},
                        'photo': {'required': False}}

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            # If 'password' is provided, update it
            password = validated_data['password']
            instance.set_password(password)
        if 'FullName' in validated_data:
            instance.FullName = validated_data.get('FullName', instance.FullName)
        if 'photo' in validated_data:
            instance.photo = validated_data.get('photo', instance.photo)


        # Update other fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # Set the password using the set_password method for proper hashing

        instance.save()
        return instance
    
    
   


