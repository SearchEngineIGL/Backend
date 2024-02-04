
from rest_framework import serializers
from .models import *
from authenticationApp.managers import *
from authenticationApp.serializers import *



"""_summary_

    Serialzer Class to manipulate Moderator objects
    """
        
class ModifyModeratorSerializer(serializers.ModelSerializer):
    
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