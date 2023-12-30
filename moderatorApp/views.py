from django.shortcuts import render
from moderatorApp.permissions import IsModeratorUser
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from authenticationApp.utils import *
from .permissions import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required



@api_view(['GET'])
def welcomeModerator(request):
    return Response({'message':"Welcome moderator ! "})




@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated,IsModeratorUser])
def ModeratorSettings(request):
    user = request.user
    if request.method == 'GET':
        serializer = ModifyModeratorSerializer(user)
        return Response(serializer.data)

    if request.method=='PUT':
        data=request.data
        serializer=ModifyModeratorSerializer(user,data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)