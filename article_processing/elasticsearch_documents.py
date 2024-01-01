# # elasticsearch_documents.py
# from elasticsearch_dsl import Document, Text, Keyword
# from elasticsearch_dsl.connections import connections

# from tpGL import settings  # Adjust this import based on your project structure

# # Use the configured Elasticsearch connection from settings
# elasticsearch_hosts = settings.ELASTICSEARCH_DSL.get('hosts', [])

# # Create the Elasticsearch connection
# connections.create_connection(hosts=elasticsearch_hosts)
# class ArticleDocument(Document):
#     title = Text()
#     content = Text()
#     is_published = Keyword()

#     class Index:
#         name = 'articles'  # Replace with your actual index name

#     def save(self, **kwargs):
#         """
#         Save the document to Elasticsearch.

#         Parameters:
#         - **kwargs: Additional keyword arguments.

#         Returns:
#         - A response from Elasticsearch indicating the result of the save operation.
#         """
#         return super(ArticleDocument, self).save(**kwargs)

# article_processing/elasticsearch_documents.py

# from django_elasticsearch_dsl import Document, Text, Keyword
# from django_elasticsearch_dsl.registries import registry
# from .models import Article
# @registry.register_document
# class ArticleDocument(Document):
#     title = Text()
#     abstract = Text()
#     keywords = Keyword(multi=True)
#     authors = Keyword(multi=True)
#     content = Text()

#     class Index:
#         name = 'article_index'  # Index name in Elasticsearch
#     class Django:
#         model = Article  # Replace YourModel with your actual Django model
#         fields = [
#             # List the fields you want to include in the Elasticsearch index
#             'title',
#             'abstract',
#             'keywords',
#             'authors',
#             'content',
#             # ...
#         ]

# documents.py
from elasticsearch_dsl import Document, Text, Keyword

# class ArticleDocument(Document):
#     title = Text()
#     authors = Keyword(multi=True)
#     # institutions = Keyword(multi=True)
#     abstract = Text()
#     keywords = Keyword(multi=True)
#     content = Text()
#     # refrences = Keyword(multi=True)

#     class Index:
#         name = 'article'
