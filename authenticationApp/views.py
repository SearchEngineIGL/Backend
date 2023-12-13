from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .utils import send_code_to_user

@api_view(['POST'])
def Register(request):
    if request.method == 'POST':
        serializer=SimpleUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=serializer.data
            send_code_to_user(user['email'])
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def LogIn(request):
    if request.method=='POST':
        email=request.data.get('email')
        password=request.data.get('password')
        user=authenticate(email=email,password=password)
        if user :
            token=Token.objects.get_or_create(user=user)
            return Response({'token':token.key},status=status.HTTP_200_OK)
        return Response({'error':'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)