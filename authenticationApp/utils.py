import random
from django.core.mail import EmailMessage
from .models import OneTimePassword,CustomUser



def generateOtp():
    otp=""
    for i in range(6):
        otp+=str(random.randint(1,9))
    return otp

def send_code_to_user(email):
    Subject="One time pascode for Email verification"
    otp_code=generateOtp()
    print (otp_code)
    user=CustomUser.objects.get(email=email)
    current_site="SearchEngine.com"
    email_body= f"Salam,\n thanks for signing up on {current_site} please verify your email with the \n one time passcode {otp_code}"
    from_email="enginesearch865@gmail.com"
    OneTimePassword.objects.create(user=user,code=otp_code)
    send_email=EmailMessage(subject=Subject,body=email_body,from_email=from_email,to=[email])
    send_email.send(fail_silently=True)