from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .utils import send_code_to_user
from .models import OneTimePassword,CustomUser
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator


@api_view(['POST'])
@permission_classes([AllowAny]) 
def Register(request):
    
    """_summary_

    Register view to send the data to the front end 
    """
    if request.method == 'POST':
        serializer=RegisterSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            user=serializer.data
            send_code_to_user(user['email'])
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


  
@api_view(['POST'])
@permission_classes([AllowAny]) 
def VerifyUserEmail(request):
    """_summary_

    Email Verification view to send the data to the front end 
    """
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
@permission_classes([AllowAny]) 
def LogIn(request):
    """_summary_

   Log In view to send the data to the front end 
    """  
    if request.method=='POST':
        serializer=LoginSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

@api_view([('POST')])
@permission_classes([AllowAny]) 
def PasswordReset(request):
    """_summary_

    Password Reset view to send the data to the front end 
    """  
    if request.method=="POST":
        serializer=PasswordResetRequestSerializer(data=request.data,context={'request':request})
        print('hello')
        serializer.is_valid(raise_exception=True)
        email=request.data.get('email')
        user=CustomUser.objects.get(email=email)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response({'message':'A link has been sent to your email to reset your password . '},status=status.HTTP_200_OK)



@api_view([('GET')])
@permission_classes([AllowAny]) 
def PasswordResetConfirm(request,uidb64,token):
    """_summary_

    Password Reset Confirmation view to get the data (code) to the front end 
    """    
    if request.method=='GET':
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'message':'token is invalid or has expired'},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True,'message':'credentials is valid','uidb64':uidb64,'token':token},status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'message':'token is invalid or has expired'},status=status.HTTP_401_UNAUTHORIZED)
        
  
@api_view(['PATCH'])
@permission_classes([AllowAny]) 
def SetNewPassword(request):
          
    """_summary_

    New password  view to modify the new password  
    """  
    serializer=SetNewPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'message':'passwordreset successully'},status=status.HTTP_200_OK)
  
@api_view(['POST'])
@permission_classes([AllowAny]) 
def LogoutUser(request):
    
    """_summary_

    Log out  view to send the data to the front end 
    """
    if request.method=='POST':
        serializer=LogoutUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    