# # # # elasticsearch_utils.py
# # # from elasticsearch import Elasticsearch

# # # es = Elasticsearch()

# # # def save_to_elasticsearch(article_data):
# # #     # Your Elasticsearch indexing logic here
# # #     es.index(index='articles', body=article_data)

# # # def publish_to_users(article_id):
# # #     # Your Elasticsearch update logic here
# # #     es.update(index='articles', id=article_id, body={'doc': {'is_published': True}})
# # # # elasticsearch_utils.py

# # from elasticsearch_dsl.connections import connections
# # from .elasticsearch_documents import ArticleDocument

# # from tpGL import settings  # Adjust this import based on your project structure

# # # Use the configured Elasticsearch connection from settings
# # elasticsearch_hosts = settings.ELASTICSEARCH_DSL.get('hosts', [])

# # # Create the Elasticsearch connection
# # connections.create_connection(hosts=elasticsearch_hosts)

# # def index_document(index_name, document_id, title, content, is_published):
# #     """
# #     Index a document in Elasticsearch using Elasticsearch DSL.

# #     Parameters:
# #     - index_name: The name of the Elasticsearch index.
# #     - document_id: The unique identifier for the document.
# #     - title: The title of the document.
# #     - content: The content of the document.
# #     - is_published: The publication status of the document.

# #     Returns:
# #     - True if the indexing was successful, False otherwise.
# #     """
# #     try:
# #         article = ArticleDocument(
# #             meta={'id': document_id, 'index': index_name},
# #             title=title,
# #             content=content,
# #             is_published=is_published
# #         )
# #         article.save()
# #         return True
# #     except Exception as e:
# #         print(f"Error indexing document: {e}")
# #         return False
# # article_processing/elasticsearch_utils.py

# from .elasticsearch_documents import ArticleDocument
#from .models import Article


# def index_article(pdf_name, article_info):
#     # Create an instance of the Article class
#     article = Article(
#         title=article_info['title'],
#         abstract=article_info['abstract'],
#         keywords=article_info['keywords'],
#         authors=article_info['authors'],
#         content=article_info['content']
#     )

#     # Create an instance of the ArticleDocument class
#     article_doc = ArticleDocument(
#         meta={'id': pdf_name},
#         title=article.title,
#         abstract=article.abstract,
#         keywords=article.keywords,
#         authors=article.authors,
#         content=article.content
#     )

#     # Index the article into Elasticsearch
#     article_doc.save()

# # Usage example
# articles_dict = {
#     'pdf1': {'title': 'Title1', 'abstract': 'Abstract1', 'keywords': ['key1', 'key2'], 'authors': ['author1'], 'content': 'Content1'},
#     'pdf2': {'title': 'Title2', 'abstract': 'Abstract2', 'keywords': ['key3', 'key4'], 'authors': ['author2'], 'content': 'Content2'},
#     # Add more articles as needed
# }

# for pdf_name, article_info in articles_dict.items():
#     index_article(pdf_name, article_info)
from elasticsearch_dsl.connections import connections
from elasticsearch_documents import ArticleDocument
from elasticsearch_dsl import Search

es = connections.create_connection(hosts=['http://localhost:9200'], http_auth= ['elastic', 'nes2504rine'],)

# # Assuming articles_data is a list of dictionaries representing articles
# articles_data = [
#     {"title": "Title 1", "abstract": "Abstract 1", "keywords": ["key1", "key2"], "authors": ["author1", "author2"], "content": "Content 1"},
#     {"title": "Title 2", "abstract": "Abstract 2", "keywords": ["key3", "key4"], "authors": ["author3", "author4"], "content": "Content 2"},
#     {"title": "Title 3", "abstract": "Abstract 3", "keywords": ["key5", "key6"], "authors": ["author5", "author6"], "content": "Content 3"},
#     # Add more articles as needed
# ]

# for article_data in articles_data:
#     ArticleDocument(**article_data).save()

# from elasticsearch import Elasticsearch

# # Connect to Elasticsearch
# es = Elasticsearch(['http://localhost:9200'], http_auth=['elastic', 'nes2504rine'])

# def update_document(index, doc_id, new_data):
#     """
#     Update a document in the specified index.

#     Parameters:
#     - index: The index where the document is stored.
#     - doc_id: The ID of the document to be updated.
#     - new_data: A dictionary containing the new data to be added or updated in the document.
#     """
#     try:
#         # Use the update API to update the document
#         es.update(index=index, id=doc_id, body={"doc": new_data})
#         print(f"Document with ID {doc_id} updated successfully.")
#     except Exception as e:
#         print(f"Error updating document: {e}")
        



# # Connect to Elasticsearch
# es = Elasticsearch(['http://localhost:9200'])

# def update_article(index, doc_id, new_data):
#     # Get the existing document
#     existing_doc = ArticleDocument.get(index=index, id=doc_id)

#     # Update the document fields
#     for field, value in new_data.items():
#         setattr(existing_doc, field, value)

#     # Save the updated document
#     existing_doc.save()
#     print(f"Article with ID {doc_id} updated successfully.")
# articles_data = [
#     {"title": "Title 1", "abstract": "Abstract 1", "keywords": ["key1", "key2"], "authors": ["author1", "author2"], "content": "Content 1"},
#     {"title": "Title 2", "abstract": "Abstract 2", "keywords": ["key3", "key4"], "authors": ["author3", "author4"], "content": "Content 2"},
#     {"title": "Title 3", "abstract": "Abstract 2", "keywords": ["key3", "key4"], "authors": ["author3", "author4"], "content": "Content 2"},
#     # Add more articles as needed
# ]  
# def add_article(index, article_data):
#     # Create a new ArticleDocument instance
#     new_article = ArticleDocument(**article_data)

#     # Save the new document
#     new_article.save()
#     print(f"New article added successfully.")

# # Example usage:
# new_article_data = {
#     "title": "New Title",
#     "abstract": "New Abstract",
#     "keywords": ["new_key1", "new_key2"],
#     "authors": ["new_author1", "new_author2"],
#     "content": "New Content"
# }
# add_article(index='article', article_data=new_article_data)

def delete_article(index, doc_id):
    # Get the existing document
    existing_doc = ArticleDocument.get(index=index, id=doc_id)

    # Delete the document
    existing_doc.delete()
    print(f"Article with ID {doc_id} deleted successfully.")

# Example usage:
delete_article(index='article_index', doc_id='CqAJvYwBFg6TbgZinlaX')


# # Example usage:
# update_data = {"title": "Updated Title", "abstract": "Updated Abstract"}
# update_article(index='article_index', doc_id='CqAJvYwBFg6TbgZinlaX', new_data=update_data)


# # Example of updating a document with ID '1' in the 'article_index'
# update_data = {"references": "New Value", "title": "title 6"}
# update_document(index='article_index', doc_id='1', new_data=update_data)







def search(data):
    if __name__ == "__main__":
         res=Search(index=index_name).using(client).query("multi_match",fuzziness="AUTO",query=data)
    return res


def filtrer(criterias , articles ):
     result =None 
# test2.query("match", fam_name="dehili").execute()
     if (criterias != None ) :
        if( "title" in criterias)  :
               result=articles.query("match", title=criterias["title"])
        if("abstract" in criterias ) :
                if(result!=None) :
                   result=(result.query("match", abstract=criterias["abstract"]))
                else :
                  result=(articles.query("match", abstract=criterias["abstract"]))    
        if("keywords" in criterias ) :
                if(result!=None) :
                   result=(result.query("match", keywords=criterias["keywords"]))
                else :
                 result=(articles.query("match", keywords=criterias["keywords"]))
        if("authors" in criterias ) :
                if(result!=None) :
                   result=(result.query("match", authors=criterias["authors"]))
                else :
                 result=(articles.query("match", authors=criterias["authors"]))
        if("content" in criterias ) :
                if(result!=None) :
                   result=(result.query("match", content=criterias["content"]))
                else :
                 result=(articles.query("match", content=criterias["content"]))

                 
        return result
     else :
        return articles
