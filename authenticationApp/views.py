from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def Register(request):
    serializer=SimpleUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def some(request):
    users=SimpleUser.objects.all()
    serializer=SimpleUserSerializer(users,many=True)
    return Response(serializer.data)