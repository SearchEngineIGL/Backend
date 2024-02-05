# views.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def welcomeElasticSearch(request):
    return Response({'message':"Welcome to elastic search ! "})


# def search_view(request):
#     return render(request, 'search_test.html')