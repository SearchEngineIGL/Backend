"""
Admin module contains all the functions related to the admin functionnalities  
    """  



from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from .pdf_extraction import *
from article_processing.elasticsearch_utils import *
import random
from elasticsearch import Elasticsearch
from django.core.mail import EmailMessage
ELASTICSEARCH_HOST = 'http://localhost:9200'
ELASTICSEARCH_USERNAME = 'elastic'  
ELASTICSEARCH_PASSWORD = 'nes2504rine'
INDEX_NAME='articles_index'



def send_moderator_email(data):
    """_summary_
    function to send to the moderator an email 
    """
    email=EmailMessage(
        subject="You're a moderator now ! ",
        body="Salam Alaikoum, \nCongratulations! you've been added as moderator in Ctrl F website ! \nYou can access with these credentials : \nemail : "+data['email']+"\nPassword : "+data['username']+"\nPlease, change the password as soon as possible.\nThanks." ,
        from_email="enginesearch865@gmail.com",
        to=[data['email']],
    )
    email.send()



def send_moderator_email_modify(data):
    """_summary_
function to send to the moderator an email to tell him we modifie his information
    """  
    email=EmailMessage(
        subject="Informations Changed ",
        body="Salam Alaikoum, \nYour informations has been changed, you can find here the new ones : \n"+"Username : "+data['username']+"\n"+"Email : "+data['email']+"\nThanks." ,
        from_email="enginesearch865@gmail.com",
        to=[data['email']],
    )
    email.send()
  


def send_moderator_email_delete(email):
    """_summary_
function to send to the moderator an email to tell him that he is deleted from the moderator role
    """  
    email=EmailMessage(
        subject="You're no more moderator ! ",
        body="Salam Alaikoum, \nWe regret to inform you that, with sincere apologies, you have been removed from the list of moderators.\nKind regards." ,
        from_email="enginesearch865@gmail.com",
        to=[email],
    )
    email.send()
    

def extraire_id_dossier_google_drive(url):
    """_Function to get the id of a google drive folder _
    """
    if "drive.google.com" in url and "/folders/" in url:
        debut_id = url.find("/folders/") + len("/folders/")
        fin_id = url.find("/", debut_id)
        if fin_id == -1:
            fin_id = None
        dossier_id = url[debut_id:fin_id]
        return dossier_id
    else:
        print("URL invalide. Assurez-vous qu'il s'agit d'un lien vers un dossier Google Drive.")
        return None

def lister_fichiers_dans_Drive(folder_id):
    
    """_Function to get all the pdf files existing in  google drive folder _
"""
    
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authentification via un serveur Web local
    drive = GoogleDrive(gauth)

    # Liste des fichiers dans le dossier spécifié
    folder_files = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    

    return folder_files


def get_next_article_id(es, index_name):
    
    """_summary_
    function return the id of the new article added in the index 
    """
    # Get the count of existing articles in Elasticsearch
    count_response = es.count(index=index_name)
    existing_articles_count = count_response["count"]

    # Return the next available article ID (increment by 1)
    return existing_articles_count + 1


def get_list_extractedFiles(link):
    
 """_summary_
function to get all the articles existing in the drive link and extract each pdf using the extraction method
"""
 list_articles=[]
 dossier_id = extraire_id_dossier_google_drive(link)

 if dossier_id:
    print(f"ID du dossier Google Drive extrait : {dossier_id}")
 else:
    print("Impossible d'extraire l'ID du dossier Google Drive.")

 liste_fichiers = lister_fichiers_dans_Drive(dossier_id)  
 article_id=retrieve_last_article_id()
 
 if article_id==None:
     article_id=1
 else:
    article_id = str(int(article_id) + 1)
    
 
 if liste_fichiers:
    
    # print("Liste des fichiers dans le dossier :")
    for fichier in liste_fichiers:
        # Use 'webContentLink' for direct download link
        pdf_url = fichier['webContentLink']
        result=extract_article_pdf(pdf_path=pdf_url,article_id=article_id)
        article_id = str(int(article_id) + 1)
        list_articles.append(result)       
 else:
    print("Aucun fichier trouvé dans le dossier.")
 return(list_articles)




