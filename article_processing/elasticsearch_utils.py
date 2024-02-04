from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Q
from elasticsearch_dsl import Search
from datetime import datetime


# from adminApp.utils import get_list_extractedFiles
# Replace with your Elasticsearch server information
ELASTICSEARCH_HOST = 'http://localhost:9200'
ELASTICSEARCH_USERNAME = 'elastic'  
ELASTICSEARCH_PASSWORD = 'nes2504rine'
INDEX_NAME='articles_index2'
es = connections.create_connection(hosts=['http://localhost:9200'], http_auth= ['elastic', 'nes2504rine'],)
# # Define your list of articles
# articles = [
#     {"article_id":1,"title": "Article 1", "content": "This is the content of Article 1.", "author": "John Doe"},
#     {"article_id":2,"title": "Article 2", "content": "This is the content of Article 2.", "author": "Jane Smith"},
#     {"article_id":2,"title": "Article 3", "content": "This is the content of Article 2.", "author": "Jane Smith"},
    
# ]

def index_articles(articles):
    es = Elasticsearch(hosts=ELASTICSEARCH_HOST,basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD],)
    
    # Create an index (if not exists)
    index_name = INDEX_NAME

    # for article in articles:
    #      es.index(index=index_name, body=article,)
    # Index each article using article_id as the document ID
    for article in articles:
        article_id = article["article_id"]
        es.index(index=index_name, body=article, id=article_id)

# def retrieve_all_articles():
   
#     es = Elasticsearch(hosts=ELASTICSEARCH_HOST,basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD],)
#     # Replace 'articles_index' with your actual index name
#     index_name = INDEX_NAME

#     # Check if the index exists
#     if es.indices.exists(index=index_name):
#         # Use the search API to retrieve all documents
#         search_result = es.search(index=index_name, body={"query": {"match_all": {}}})

#         # Display the retrieved articles
#         for hit in search_result['hits']['hits']:
#             article = hit['_source']
#             print(f"Title: {article.get('title')}, Content: {article.get('content')}, Author: {article.get('author')}")
            

def retrieve_all_articles_list():
    articles=[]
    es = Elasticsearch(hosts=ELASTICSEARCH_HOST,basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD],)
    # Replace 'articles_index' with your actual index name
    index_name = INDEX_NAME

    # Check if the index exists
    if es.indices.exists(index=index_name):
        # Use the search API to retrieve all documents
        search_result = es.search(index=index_name, body={"query": {"match": {"state": "pending"}}})
        # Display the retrieved articles
        for hit in search_result['hits']['hits']:
            article = hit['_source']
            article_id = hit['_id']  # Retrieve the article ID
            article_title = article.get('title')
            state = article.get('state')  # Assuming there is a field named 'status'
            url = article.get('url')  # Assuming there is a field named 'status'

            # Add the article details to the list
            articles.append({"article_id": article_id, "article_title": article_title,"state": state,"url":url})

    
    return(articles)   
        

def delete_article_by_custom_id(article_id):
    es = Elasticsearch(hosts=ELASTICSEARCH_HOST,basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD],)
    # Replace 'articles_index' with your actual index name
    index_name = INDEX_NAME
    # Check if the index exists
    if es.indices.exists(index=index_name):
        try:
            # Use the search API to find documents with the specified article_id
            search_result = es.search(index=index_name, body={
                "query": {"term": {"article_id": article_id}},
                "size": 1
            })

            # Check if any documents were found
            if search_result['hits']['hits']:
                document_id = search_result['hits']['hits'][0]['_id']

                # Use the delete API to delete the specified article by ID
                es.delete(index=index_name, id=document_id)
                print(f"Article with custom ID {article_id} deleted successfully.")
            else:
                print(f"No article found with custom ID {article_id}.")
        except Exception as e:
            print(f"Error deleting article with custom ID {article_id}: {e}")
    else:
        print(f"Index {index_name} does not exist.")

def retrieve_last_article_id():
    es = Elasticsearch(hosts=ELASTICSEARCH_HOST,basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD],)
    # Replace 'articles_index' with your actual index name
    index_name = INDEX_NAME

    # Check if the index exists
    if es.indices.exists(index=index_name):
        # Use the search API to retrieve the last article's ID based on the article_id field
        search_result = es.search(index=index_name, body={
            "query": {"match_all": {}},
            "size": 1,
            "sort": [{"article_id": {"order": "desc"}}]
        })

        # Extract the last article's ID
        if search_result['hits']['hits']:
            last_article_id = search_result['hits']['hits'][0]['_source'].get('article_id')
            return last_article_id
        else:
            print("No articles found.")
            return None
    else:
        print(f"Index {index_name} does not exist.")
        return None

def add_new_articles(articles):
    es = Elasticsearch(hosts=ELASTICSEARCH_HOST,basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD],)
    # Replace 'articles_index' with your actual index name
    index_name = INDEX_NAME
    # Retrieve the last article's ID
    last_article_id = retrieve_last_article_id()

    # Use the index API to add the new articles to Elasticsearch
    try:
        for article in articles:
            # Increment the article_id based on the last_article_id
            article['article_id'] = last_article_id + 1 if last_article_id is not None else 1
            response = es.index(index=index_name, body=article, id=article['article_id'])
            print(f"Article added successfully with ID: {response['_id']}")
            last_article_id = article['article_id']  # Update last_article_id for the next iteration
    except Exception as e:
        print(f"Error adding new articles: {e}")



def update_article_by_custom_id(article_id, updated_fields):
    es = Elasticsearch(hosts=ELASTICSEARCH_HOST,basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD],)
    # Replace 'articles_index' with your actual index name
    index_name = INDEX_NAME

    # Check if the index exists
    if es.indices.exists(index=index_name):
        try:
            # Use the search API to find documents with the specified article_id
            search_result = es.search(index=index_name, body={
                "query": {"term": {"article_id": article_id}},
                "size": 1,
            })

            # Check if any documents were found
            if search_result['hits']['hits']:
                document_id = search_result['hits']['hits'][0]['_id']

                # Use the update API to update the specified fields in the article by ID
                es.update(index=index_name, id=document_id, body={
                    "doc": updated_fields
                })
                print(f"Article with custom ID {article_id} updated successfully.")
            else:
                print(f"No article found with custom ID {article_id}.")
        except Exception as e:
            print(f"Error updating article with custom ID {article_id}: {e}")
    else:
        print(f"Index {index_name} does not exist.")



def delete_index(index_name):
    
    es = Elasticsearch(hosts=ELASTICSEARCH_HOST,basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD],)
    
    # Check if the index exists
    if es.indices.exists(index=index_name):
        try:
            # Use the delete API to delete the specified index
            es.indices.delete(index=index_name)
            print(f"Index {index_name} deleted successfully.")
        except Exception as e:
            print(f"Error deleting index {index_name}: {e}")
    else:
        print(f"Index {index_name} does not exist.")
        
        
def give_article(article_id):
    es = Elasticsearch(hosts=ELASTICSEARCH_HOST, basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD])
    index_name = INDEX_NAME

    # Check if the index exists
    if es.indices.exists(index=index_name):
        # Use the get API to retrieve the document by ID
        try:
            result = es.get(index=index_name, id=article_id)
            article = result['_source']
            return article
        except Exception as e:
            print(f"Error retrieving article with ID {article_id}: {e}")
    
    return None






def search(data):
    if data is None:
        # Return all articles without applying any specific search query
        res = Search(using=es, index=INDEX_NAME).filter("term", state="done")
    else:
        # Perform a search with the provided query
        res = Search(using=es, index=INDEX_NAME).query("multi_match", fuzziness="AUTO", query=data).filter("term", state="done")
    return res



def filtrer(criterias, data):
    result = search(data)

    if criterias:
        if "keywords" in criterias and criterias["keywords"]!='':
            result = result.query(Q("match", keywords={"query": criterias["keywords"], "operator": "OR"}))
        if "author" in criterias and criterias["author"]!='':
            # Use match query for exact matching of authors
            result = result.query(Q("match", authors={"query": criterias["author"], "operator": "OR"}))
        if "institutions" in criterias and criterias["institutions"]!='':
            # Use match query for exact matching of authors
            result = result.query(Q("match", institutions={"query": criterias["institutions"], "operator": "OR"}))

        startDate = criterias.get("startDate")
        endDate = criterias.get("endDate")

        if startDate and endDate:
            start_datetime = datetime.strptime(startDate, "%Y-%m-%d")
            end_datetime = datetime.strptime(endDate, "%Y-%m-%d")
            print(startDate)
            result = result.filter("range", date={"gte": start_datetime, "lte": end_datetime})
        elif startDate:
            start_datetime = datetime.strptime(startDate, "%Y-%m-%d")
            
            result = result.filter("range", date={"gte": start_datetime})
        elif endDate:
            end_datetime = datetime.strptime(endDate, "%Y-%m-%d")
            result = result.filter("range", date={"lte": end_datetime})

    return result
    
    
    
    
def publish_article(article_id):
    es = Elasticsearch(hosts=ELASTICSEARCH_HOST,basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD],)
    # Replace 'articles_index' with your actual index name
    index_name = INDEX_NAME

    # Check if the index exists
    if es.indices.exists(index=index_name):
        try:
            # Use the search API to find documents with the specified article_id
            search_result = es.search(index=index_name, body={
                "query": {"term": {"article_id": article_id}},
                "size": 1
            })

            # Check if any documents were found
            if search_result['hits']['hits']:
                document_id = search_result['hits']['hits'][0]['_id']

                # Use the update API to update the specified fields in the article by ID
                es.update(index=index_name, id=document_id, body={
                    "state":"done"
                })
                print(f"Article with custom ID {article_id} updated successfully.")
            else:
                print(f"No article found with custom ID {article_id}.")
        except Exception as e:
            print(f"Error updating article with custom ID {article_id}: {e}")
    else:
        print(f"Index {index_name} does not exist.")




def get_articles_ordered_by_date():
    es = Elasticsearch(hosts=ELASTICSEARCH_HOST, basic_auth=[ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD])
    index_name = INDEX_NAME
    articles=[]
    try:
        # Use the search API to retrieve 5 articles ordered by the 'date' field
        search_result = es.search(
            index=index_name,
            body={
                "query": {"match_all": {}},
                "sort": [{"date": {"order": "desc"}}],  # Sort by 'date' field in descending order
                "size": 5  # Specify the number of hits to return (5 in this case)
            }
        )

        # Access the sorted articles in the search_result
        sorted_articles = search_result['hits']['hits']
        for hit in sorted_articles:
            article = hit['_source']
            article_id = hit['_id']  # Retrieve the article ID
            article_title = article.get('title')
            state = article.get('state')  # Assuming there is a field named 'status'
            url = article.get('url')  # Assuming there is a field named 'status'
            content = article.get('content')  # Assuming there is a field named 'status'
            keywords=article.get('keywords')

            # Add the article details to the list
            articles.append({"article_id": article_id, "article_title": article_title,"state": state,"url":url,"content":content,"keywords":keywords})
        return (articles)
    except Exception as e:
        print(f"Error retrieving articles: {e}")
