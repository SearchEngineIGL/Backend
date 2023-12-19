from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .utils import send_code_to_user
from .models import OneTimePassword
@api_view(['POST'])
def Register(request):
    if request.method == 'POST':
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=serializer.data
            send_code_to_user(user['email'])
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def VerifyUserEmail(request):
    if request.method=='POST':
        otpcode=request.data.get('otp')
        try :
            user_code_obj=OneTimePassword.objects.get(code=otpcode)
            user=user_code_obj.user
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({
                    'messege':"Account email verified succefully ."
                },status=status.HTTP_200_OK)
            return Response({'message':'code is invalid, user already verified'},status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({'message': 'passcode not provided'},status=status.HTTP_404_NOT_FOUND)
            
    
@api_view(['POST'])
def LogIn(request):
    if request.method=='POST':
        serializer=LoginSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)