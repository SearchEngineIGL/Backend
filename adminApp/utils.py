import random
from django.core.mail import EmailMessage
from .models import CustomUser   

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