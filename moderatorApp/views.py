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
from article_processing.elasticsearch_utils import *




@api_view(['GET'])
def welcomeModerator(request):
    return Response({'message':"Welcome moderator ! "})




"""_summary_

    Moderator   view to send the data and get the data from the front end
    """
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



"""_summary_

    Articles list view to send the data to the front end for correction method
    """
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsModeratorUser])
def display_articles_for_correction(request):
    if request.method =='GET':
        articles = retrieve_all_articles_list()
        return Response(articles,status=status.HTTP_200_OK)



"""_summary_

    Article  view to send the data to the front end and get the new correction ones  
    """
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated,IsModeratorUser])
def CorrectionArticle(request,article_id):
    if request.method=='GET':
        article=give_article(article_id)
        return Response(article)
    if request.method=='PUT':
        data=request.data
        update_article_by_custom_id(article_id,data)
        return Response(status=status.HTTP_200_OK)



"""_summary_

    Article view to delete the article if it is full of mistakes 
    """
@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsModeratorUser])
def deleteArticle(request,article_id):
  if request.method=='DELETE':
    delete_article_by_custom_id(article_id)
    return Response(status=status.HTTP_204_NO_CONTENT)

"""_summary_

    Article view to publish an article 
    """

@api_view(['PATCH'])
@permission_classes([IsAuthenticated,IsModeratorUser])
def publishAricle(request,article_id):
  if request.method=='PATCH':
    publish_article(article_id)
    return Response(status=status.HTTP_200_OK)
