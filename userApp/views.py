from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from authenticationApp.utils import *
from .permissions import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

@api_view(['GET'])
def welcomeUser(request):
    return Response({'message':"Welcome User ! "})








