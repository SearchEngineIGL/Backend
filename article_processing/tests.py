import unittest
from unittest.mock import patch, MagicMock
from elasticsearch_utils import index_articles  


class IndexArticlesTestCase(unittest.TestCase):
    
    """_Unit test for testing the function of indexing articles in elastic search_
    """

    @patch('elasticsearch_utils.Elasticsearch')  
    def test_index_articles(self, mock_elasticsearch):
        # Mock the Elasticsearch object
        es_instance = mock_elasticsearch.return_value
        es_instance.index = MagicMock()

        # Sample articles for testing
        articles = [
            {"article_id": 1, "title": "Article 1", "content": "Content 1"},
            {"article_id": 2, "title": "Article 2", "content": "Content 2"},
            # Add more sample articles as needed
        ]

        # Call the function to be tested
        index_articles(articles)

        # Assert that the Elasticsearch index method was called for each article
        for article in articles:
            es_instance.index.assert_any_call(
                index='articles_index',  
                body=article,
                id=article["article_id"]
            )

if __name__ == '__main__':
    unittest.main()
