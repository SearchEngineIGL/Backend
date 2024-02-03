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
from article_processing.elasticsearch_utils import filtrer, search

# request.query_params
# @api_view(['POST'])
# def search_view(request):
#     if request.method == 'POST':
#         dataInput = request.data.get("query")
#         # Call your Elasticsearch function with the user input
#         search_results = search(dataInput)
#         results_list = []
#         for hit in search_results.execute():
#             results_list.append(hit.to_dict())

#         return Response(results_list,status=status.HTTP_200_OK)

#     return JsonResponse({'error': 'Invalid request method'})


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsSimpleUser])
def search_view(request,query):
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
            print(criteria)
            
        search_results = search(query)
        if criteria:
            search_results2 = filtrer(criteria, search_results)
            print(search_results2)
        results_list = []
        for hit in search_results2.execute():
            results_list.append(hit.to_dict())
        print(results_list)
        return Response(results_list, status=status.HTTP_200_OK)

    return JsonResponse({'error': 'Invalid request method'})

@api_view(['GET'])
def welcomeUser(request):
    return Response({'message':"Welcome User ! "})



