from .views import *
from django.urls import path

urlpatterns = [
    path('register/',Register),
    path('login/',LogIn),
    path('verifyEmail/',VerifyUserEmail),    
    path('password-reset/',PasswordReset),    
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirm,name='password-reset-confirm'),    
    path('set-new-password/',SetNewPassword),    
]
