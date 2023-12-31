# views.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def welcomeElasticSearch(request):
    return Response({'message':"Welcome to elastic search ! "})

# from .elasticsearch_utils import index_document

# def process_article(article_id, title, content):
#     # Define your Elasticsearch index name
#     index_name = 'articles'

#     # Example call to index a document
#     success = index_document(
#         index_name=index_name,
#         document_id=article_id,
#         title=title,
#         content=content,
#         is_published=False  # Adjust based on your needs
#     )

#     if success:
#         print(f"Successfully indexed document with ID: {article_id}")
#     else:
#         print(f"Failed to index document with ID: {article_id}")

