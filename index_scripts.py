# index_articles_script.py
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from article_processing.elasticsearch_documents import ArticleDocument

# Fetch or generate your articles data
articles_data = [
    {"title": "Title 1", "abstract": "Abstract 1", "keywords": ["key1", "key2"], "authors": ["author1", "author2"], "content": "Content 1"},
    {"title": "Title 2", "abstract": "Abstract 2", "keywords": ["key3", "key4"], "authors": ["author3", "author4"], "content": "Content 2"},
    # Add more articles as needed
]

# Elasticsearch configuration
es = Elasticsearch(['localhost:9200'])  # Replace with your Elasticsearch server details

# Create an index (if not exists)
index_name = 'article_index'
ArticleDocument.init(index=index_name, using=es)

# Index the articles
actions = [
    {
        "_op_type": "index",
        "_index": index_name,
        "_source": article_data
    }
    for article_data in articles_data
]

# Use the bulk helper to perform the indexing
success, failed = bulk(es, actions)

# Print the results
print(f"Successfully indexed {success} articles.")
print(f"Failed to index {failed} articles.")
