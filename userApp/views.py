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












from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.http import JsonResponse
from article_processing.elasticsearch_utils import filtrer

# request.query_params
@api_view(['POST'])
def search_view(request):
    if request.method == 'POST':
        # Get the text entered by the user from the request
        user_input = request.POST.get('user_input', '')
        print(user_input)
        # Call your Elasticsearch function with the user input
        # search_results = search(user_input)

        # return JsonResponse({'results': search_results})
        return JsonResponse({'results': "corrrecttt"})
    return JsonResponse({'error': 'Invalid request method'})




# here are the necessary modifications of the search function in the front end
# const handleSearch = async (textInput) => {
#     try {
#         const response = await axios.post('/your-django-app/search/', { user_input: textInput });
#         const searchResults = response.data.results;
#         // Process the search results as needed
#     } catch (error) {
#         console.error('Error while making search request:', error);
#     }
# };


@api_view(['GET'])
def welcomeUser(request):
    return Response({'message':"Welcome User ! "})









# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import Student
# from .serializers import StudentSerializer
# from elasticsearch_dsl import Search
# from elasticsearch_dsl.query import Q

# class Search(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     @action(detail=False, methods=['get'])
#     def search_students(self, request):
#         gender = request.query_params.get('gender')
#         study = request.query_params.get('study')

#         # Build Elasticsearch query based on filters
#         search_query = Search(index='your_index')  # Replace 'your_index' with your Elasticsearch index name

#         if gender:
#             search_query = search_query.query('match', gender=gender)

#         if study:
#             search_query = search_query.query('match', study=study)

#         # Execute the Elasticsearch query
#         response = search_query.execute()

#         # Process the response as needed
#         results = [{'id': hit.meta.id, 'source': hit.to_dict()} for hit in response]

#         return Response(results)

