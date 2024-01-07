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
from article_processing.elasticsearch_utils import *


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



@api_view(['GET'])
@permission_classes([IsAuthenticated,IsModeratorUser])
def display_articles_for_correction(request):
    if request.method =='GET':
        articles = retrieve_all_articles_list()
        return Response(articles,status=status.HTTP_200_OK)


def CorrectionArticle(request,article_id):
  existing_articles = retrieve_all_articles_list()  # Retrieve all articles or filter as needed
  existing_article = None
  for article in existing_articles:
        if article.get('article_id') == article_id:
            existing_article = article
            break
        update_article_by_custom_id(article_id,any)


def deleteArticle(request,article_id):

  delete_article_by_custom_id(article_id)

    