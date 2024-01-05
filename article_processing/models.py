

# Create your models here.
# article_processing/models.py

class Article:
    def __init__(self, title, abstract, keywords, authors, content):
        self.title = title
        self.abstract = abstract
        self.keywords = keywords
        self.authors = authors
        self.content = content
