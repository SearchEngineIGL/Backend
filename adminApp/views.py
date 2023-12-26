from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from authenticationApp.utils import *
from rest_framework import status
from .utils import *

@api_view(['GET'])
def welcomeAdmin(request):
    return Response({'message':"Welcome Admin ! "})

@api_view(['POST'])
def create_moderator(request):
    if request.method == 'POST':
        serializer=CreateModeratorserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=serializer.data
            user_data={'username': user['username'], 'email': user['email']}
            send_moderator_email(user_data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_of_moderators(request):
    if request.method =='GET':
        moderators=CustomUser.objects.filter(user_type="moderator")
        serializer=CustomUserSerializer(moderators,many=True)
        return Response(serializer.data)
    
@api_view(['PUT'])
def MAJ_moderator(request,id):
    if request.method=='PUT':
        try: 
            user=CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=CustomUserSerializer(user,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            
@api_view(['DELETE'])
def Delete_moderator(request,id):
    if request.method=='DELETE':
        try: 
            user=CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist():
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
            