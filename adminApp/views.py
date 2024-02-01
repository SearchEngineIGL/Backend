from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from .serializers import *
from authenticationApp.utils import *
from rest_framework import status
from .utils import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from .serializers import *

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def welcomeAdmin(request):
    return Response({'message':"Welcome Admin ! "})


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def create_moderator(request):
    
    if request.method == 'POST':
        serializer=CreateModeratorserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=serializer.data
            user_data={'username': user['username'], 'email': user['email']}
            send_moderator_email(user_data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def list_of_moderators(request):
    if request.method =='GET':
        moderators=CustomUser.objects.filter(user_type="moderator")
        serializer=CustomUserSerializer(moderators,many=True)
        return Response(serializer.data)
    
    
@api_view(['PUT','GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def MAJ_moderator(request,id):
    try: 
        user=CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    if request.method=='PUT':
        
        serializer=CustomUserSerializer(user,request.data)
        if serializer.is_valid():
            serializer.save()
            send_moderator_email_modify(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def Delete_moderator(request,id):
    if request.method=='DELETE':
        try: 
            user=CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist():
            return Response(status=status.HTTP_404_NOT_FOUND)
        email=user.email
        user.delete()
        send_moderator_email_delete(email)
        return Response(status=status.HTTP_204_NO_CONTENT)
            
            


@api_view(['PUT','GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def AdminSettings(request):
    admin_user=request.user
    if request.method == 'GET':
        serializer = ModifyAdminSerializer(admin_user)
        return Response(serializer.data)

    if request.method=='PUT':
        
        admin_user=request.user
        data=request.data
        serializer=ModifyAdminSerializer(admin_user,data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


# @api_view(['POST'])
# @permission_classes([IsAuthenticated, IsAdminUser])
# def upload_articles_from_url(request):
#     if request.method == 'POST':
#         url = request.data.get('url')
        
#         # Fetch articles from the provided URL
#         response = requests.get(url)
        
#         articles_data = get_list_extractedFiles(response.content)
#         if(articles_data==None):
#             return Response( status=status.HTTP_400_BAD_REQUEST)
        
#         return Response(status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_articles(request):
    
    if request.method == 'POST':
        serializer=GetUrlSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':"correct link"},status=status.HTTP_200_OK)
    return Response({'message': 'Invalid request method'}, status=400)

@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    print(csrf_token)
    return Response({'csrf_token': csrf_token})
# views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import LinkSerializer
# @csrf_exempt
# class GetLink(APIView):
    
    
#     def post(self, request, format=None):
#         # Deserialize the incoming data using the LinkSerializer
#         serializer = LinkSerializer(data=request.data)
#         if serializer.is_valid():
#             # Get the validated link value
#             validated_link = serializer.validated_data['link']

#             # Process the link, save it to ElasticSearch, etc.
#             # Your logic here...

#             return Response({'message': 'Link saved successfully'}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
