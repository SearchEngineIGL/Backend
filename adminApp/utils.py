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
    
