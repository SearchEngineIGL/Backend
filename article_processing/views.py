from django.shortcuts import render

# Create your views here.
# views.py
# views.py

from elasticsearch_documents import create_article_document
from elasticsearch_utils import save_to_elasticsearch

def process_article(title, content):
    # Create an Elasticsearch document
    article_document = create_article_document(
        title=title,
        content=content
    )

    # Save to Elasticsearch
    save_to_elasticsearch(article_document)
