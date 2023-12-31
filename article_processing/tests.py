# from django.test import TestCase

# # Create your tests here.
# # test_search.py

# from elasticsearch import Elasticsearch

# # Assuming your Elasticsearch server is running on 'localhost:9200'
# es = Elasticsearch(hosts=['http://localhost:9200'],basic_auth=['elastic','nes2504rine'])

# # Example search query
# search_query = "Title 1"

# # Perform a search
# result = es.search(index='article_index', body={
#     'query': {
#         'match': {
#             'title': search_query
#         }
#     }
# })

# # Print the search results
# for hit in result['hits']['hits']:
#     print(f"Title: {hit['_source']['title']}, Authors: {hit['_source']['authors']}, Score: {hit['_score']}")
# from elasticsearch import Elasticsearch
# from elasticsearch_utils import update_document

# # Connect to Elasticsearch
# es = Elasticsearch(['http://localhost:9200'], http_auth=['elastic', 'nes2504rine'])

# # # Example search query to retrieve all documents
# # result = es.search(index='article_index', body={'query': {'match_all': {}}})

# # # Print the search results
# # for hit in result['hits']['hits']:
# #     print("Document:")
# #     print(hit['_source'])
# #     print("\n")
# # Example of updating a document with ID '1' in the 'article_index'
# update_data = {"references": "New Value", "title": "title 6"}
# update_document(index='article_index', doc_id='1', new_data=update_data)

from django.test import TestCase
from elasticsearch import Elasticsearch
from elasticsearch_utils import update_document  # Adjust the import path based on your actual directory structure


class YourTestCase(TestCase):
    def test_update_document(self):
        # Connect to Elasticsearch (replace with your actual Elasticsearch connection details)
        es = Elasticsearch(['http://localhost:9200'], http_auth=['elastic', 'nes2504rine'])

        # Define the update data
        update_data = {"new_field": "New Value", "updated_field": "Updated Value"}

        # Get the ID of the first document in the 'article_index'
        result = es.search(index='article_index', body={'query': {'match_all': {}}, 'size': 1})
        print("Search Result:", result)

        if result['hits']['hits']:
            doc_id = result['hits']['hits'][0]['_id']

            # Update the document
            update_document(index='article_index', doc_id=doc_id, new_data=update_data)

            # Optionally, retrieve the updated document and assert that the changes are reflected
            updated_doc = es.get(index='article_index', id=doc_id)
            self.assertEqual(updated_doc['_source']['new_field'], "New Value")
            self.assertEqual(updated_doc['_source']['updated_field'], "Updated Value")
        else:
            print("No documents found in 'article_index'")
