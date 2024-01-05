from django.test import TestCase
from unittest.mock import patch, MagicMock
from elasticsearch import Elasticsearch
from .elasticsearch_utils import (
    index_articles,
    retrieve_all_articles,
    retrieve_all_articles_list,
    delete_article_by_custom_id,
    retrieve_last_article_id,
    add_new_articles,
    update_article_by_custom_id,
    delete_index,
)


class ElasticsearchFunctionsTestCase(TestCase):
    def setUp(self):
        # Mock the Elasticsearch instance
        self.mocked_es = MagicMock(spec=Elasticsearch)
        self.mocked_es.indices.exists.return_value = True
        self.mocked_es.search.return_value = {'hits': {'hits': []}}

        # Patch the Elasticsearch instance in utils with the mocked one
        self.patcher = patch('yourapp.utils.Elasticsearch', autospec=True)
        self.mocked_es_class = self.patcher.start()
        self.mocked_es_class.return_value = self.mocked_es

    def tearDown(self):
        # Stop the patcher to restore the original state
        self.patcher.stop()

    def test_index_articles(self):
        articles = [
            {"article_id": 1, "title": "Article 1", "content": "Content 1", "author": "Author 1"},
            {"article_id": 2, "title": "Article 2", "content": "Content 2", "author": "Author 2"},
        ]

        index_articles(articles)

        # Verify that the Elasticsearch instance is created
        self.mocked_es_class.assert_called_once_with(hosts='http://localhost:9200', basic_auth=['elastic', 'nes2504rine'])

        # Verify that the es.index method was called twice with the expected arguments
        self.mocked_es.index.assert_any_call(index='articles_index', body=articles[0], id=1)
        self.mocked_es.index.assert_any_call(index='articles_index', body=articles[1], id=2)

    # Add similar test methods for other functions

    def test_delete_index(self):
        index_name = 'test_index'

        delete_index(index_name)

        # Verify that the Elasticsearch instance is created
        self.mocked_es_class.assert_called_once_with(hosts='http://localhost:9200', basic_auth=['elastic', 'nes2504rine'])

        # Verify that the es.indices.delete method was called with the expected argument
        self.mocked_es.indices.delete.assert_called_once_with(index=index_name)


# Add similar test classes for other functionalities


