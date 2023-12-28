# elasticsearch_documents.py


def create_article_document(title, content):
    """
    Create a document for indexing in Elasticsearch.
    """
    return {
        'title': title,
        'content': content,
        'is_published': False,  # You can add more fields as needed
    }

