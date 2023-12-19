from .views import *
from django.urls import path

urlpatterns = [
    path('register/',Register),
    path('login/',LogIn),
    path('verifyEmail/',VerifyUserEmail),    
]
