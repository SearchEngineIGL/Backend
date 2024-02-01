from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from .pdf_extraction import extract_article_pdf
import random
from django.core.mail import EmailMessage
# from .models import CustomUser   
# from ..article_processing.pdf_extraction import extract_article_pdf

def send_moderator_email(data):
    email=EmailMessage(
        subject="You're a moderator now ! ",
        body="Salam Alaikoum, \nCongratulations! you've been added as moderator in Ctrl F website ! \nYou can access with these credentials : \nemail : "+data['email']+"\nPassword : "+data['username']+"\nPlease, change the password as soon as possible.\nThanks." ,
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
    
"""_Function to get the id of a google drive folder_
"""
def extraire_id_dossier_google_drive(url):
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

"""_Function to get all the pdf files existing in  google drive folder_
"""
def lister_fichiers_dans_Drive(folder_id):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authentification via un serveur Web local
    drive = GoogleDrive(gauth)

    # Liste des fichiers dans le dossier spécifié
    folder_files = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

    return folder_files



def get_list_extractedFiles(link):
 list_articles=[]
 dossier_id = extraire_id_dossier_google_drive(link)

 if dossier_id:
    print(f"ID du dossier Google Drive extrait : {dossier_id}")
 else:
    print("Impossible d'extraire l'ID du dossier Google Drive.")

 liste_fichiers = lister_fichiers_dans_Drive(dossier_id)  
 article_id=1 
 if liste_fichiers:
    
    # print("Liste des fichiers dans le dossier :")
    for fichier in liste_fichiers:
        # Use 'webContentLink' for direct download link
        pdf_url = fichier['webContentLink']
        print(pdf_url)
        result=extract_article_pdf(pdf_url,article_id)
        article_id+1
        list_articles.append(result)       
 else:
    print("Aucun fichier trouvé dans le dossier.")
 return(list_articles)



# # Main
# url = "https://drive.google.com/drive/folders/1ZS68gD61U0ZOUkfj0GFcCHYqsHDVv4NX"   
# listes=get_list_extractedFiles(url)
# print(len(listes))
