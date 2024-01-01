import random
from django.core.mail import EmailMessage
# from models import CustomUser   
from pdf_extraction import extract_article_pdf

def send_moderator_email(data):
    email=EmailMessage(
        subject="You're a moderator now ! ",
        body="Salam Alaikoum, \nCongratulations! you've been added as moderator in Ctrl F website ! \nYou access with these credientials : \nemail : "+data['email']+"\nPassword : "+data['username']+"\nPlease, change the password as soon as possible.\nThanks." ,
        from_email="enginesearch865@gmail.com",
        to=[data['email']],
    )
    email.send()
    
def send_moderator_email_modify(data):
    email=EmailMessage(
        subject="Informations Changed ",
        body="Salam Alaikoum, \nYour informations has been changed, you can find here the new ones : \n"+"Username : "+data['username']+"\n"+"Email : "+data['email']+"\nThanks." ,
        from_email="enginesearch865@gmail.com",
        to=[data['email']],
    )
    email.send()
    
def send_moderator_email_delete(email):
    email=EmailMessage(
        subject="You're no more moderator ! ",
        body="Salam Alaikoum, \nWe regret to inform you that, with sincere apologies, you have been removed from the list of moderators.\nKind regards." ,
        from_email="enginesearch865@gmail.com",
        to=[email],
    )
    email.send()
    
import requests
from bs4 import BeautifulSoup  # You may need to install this library

def fetch_pdfs_from_url(url):
    # Fetch the HTML content of the URL
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all links that end with '.pdf'
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].lower().endswith('.pdf')]
   # List to store the results
    results = []
    print(len(pdf_links))
    # Iterate over PDF links and call extract_article_pdf for each
    for pdf_link in pdf_links:
        print(pdf_link)
        # Assuming extract_article_pdf is a function that processes a single PDF
        pdf_url = url + pdf_link if pdf_link.startswith('/') else pdf_link
        try:
            article_data = extract_article_pdf(pdf_url)
            results.append(article_data)
        except Exception as e:
            print(f"Error processing PDF '{pdf_url}': {e}")

    return results

# Example usage
url = 'https://drive.google.com/drive/folders/1ZS68gD61U0ZOUkfj0GFcCHYqsHDVv4NX'
result_list = fetch_pdfs_from_url(url)
print(len(result_list))
for article in result_list:
   print(article)

# Now result_list contains the processed data for each PDF
