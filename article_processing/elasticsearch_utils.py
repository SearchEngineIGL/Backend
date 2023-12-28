# elasticsearch_utils.py
from elasticsearch import Elasticsearch

es = Elasticsearch()

def save_to_elasticsearch(article_data):
    # Your Elasticsearch indexing logic here
    es.index(index='articles', body=article_data)

def publish_to_users(article_id):
    # Your Elasticsearch update logic here
    es.update(index='articles', id=article_id, body={'doc': {'is_published': True}})
