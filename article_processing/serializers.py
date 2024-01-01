# app1/serializers.py

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from elasticsearch_documents import ArticleDocument


class ArticleDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ArticleDocument
        fields = "__all__"
