from rest_framework import serializers
from .models import *
from authenticationApp.managers import *
from authenticationApp.serializers import *
from .utils import *
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
    
    
   


class GetUrlSerializer(serializers.Serializer):
    link = serializers.CharField(max_length=255)

    def validate(self, attrs):
        print("---------------------------------------")
        link = attrs.get('link')
        print('ablus')
        print(link)
        list_articles = get_list_extractedFiles(link)
        print("--------------------------------- list ----------------------------")
        print(list_articles)
        #index_articles(list_articles)
        # Additional validation or processing logic can be added here
        return attrs  # Don't forget to return the validated data


# serializers.py
# from rest_framework import serializers

# class LinkSerializer(serializers.Serializer):
#     link = serializers.URLField()
