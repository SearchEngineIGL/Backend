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
from django.http import JsonResponse
from article_processing.elasticsearch_utils import filtrer, search ,give_article,get_articles_ordered_by_date


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsSimpleUser])
def search_view(request,query):
    """_summary_

    Search view to send articles and get the request from the user  
    """
    criteria=None
    if request.method == 'GET':
        search_results = search(query)
        results_list = []
        for hit in search_results.execute():
            results_list.append(hit.to_dict())
        return Response(results_list, status=status.HTTP_200_OK)
    if request.method=='POST':
        
        if request.data!=None:
            criteria = request.data
            
        search_results = search(query)
        if criteria:
            search_results = filtrer(criteria, query)
            print(query)
            print('-------------------------')
            print(criteria)
        results_list = []
        for hit in search_results.execute():
            results_list.append(hit.to_dict())
        return Response(results_list, status=status.HTTP_200_OK)

    return JsonResponse({'error': 'Invalid request method'})

@api_view(['GET'])
def welcomeUser(request):
    return Response({'message':"Welcome User ! "})




@api_view(['GET'])
@permission_classes([IsAuthenticated,IsSimpleUser])
def ViewArticle(request,article_id):
    """_summary_

    Article view to display it to the user  
    """
    if request.method=='GET':
        article=give_article(article_id)
        return Response(article,status=status.HTTP_200_OK)
    


    
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated,IsSimpleUser])
def UserSettings(request):
    """_summary_

    User view to make modification on the user object    """   
    user = request.user
    if request.method == 'GET':
        serializer = ModifyUserSerializer(user)
        return Response(serializer.data)

    if request.method=='PUT':
        data=request.data
        serializer=ModifyUserSerializer(user,data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsSimpleUser])
def addFav(request):
    
    """_summary_

    Favors articles view to add articles to the favors list related to the user
    """
    user=request.user
    article_id = request.data.get("article_id")
    favs = user.get_additional_data().get('list_of_favorites', [])
    favs.append(article_id)
    user.set_additional_data({'list_of_favorites': favs})
    user.save()
    return Response(status=status.HTTP_201_CREATED)




@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsSimpleUser])
def rmvFav(request):
    """_summary_

    Favors articles view to remove articles to the favors list related to the user
    """    
    user=request.user
    article_id = request.data.get("article_id")
    favs = user.get_additional_data().get('list_of_favorites', [])
    if article_id in favs:
        favs.remove(article_id)
        user.set_additional_data({'list_of_favorites': favs})
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else :
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsSimpleUser])
def getFavs(request):
    """_summary_

    Favors articles view to get the list of favorite articles from user
    """  
    articles=[]
    user=request.user
    favors = user.get_additional_data().get('list_of_favorites', [])    
    print(favors)
    for element in favors:
        article=give_article(element)
        articles.append(article)
    return Response(articles,status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAuthenticated,IsSimpleUser])
def isFav(request):
    """_summary_

    Favors articles view to if the article is in favor or not
    """   
    article_id = request.data.get("article_id")
    user=request.user
    favors = user.get_additional_data().get('list_of_favorites', [])    
    if article_id in favors :
        print(article_id)
        return Response(status=status.HTTP_200_OK)    
    else :
        print('404'+article_id)
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
 
@api_view(['GET'])
def homeArticles(request):
    """_summary_

    Home article view to display all recent articles 
    """ 
    if request.method == 'GET':
        articles=get_articles_ordered_by_date()
        print(articles)
        return Response(articles, status=status.HTTP_200_OK)