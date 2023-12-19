from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken




class CustomUser(AbstractUser):
    
    USER_TYPE_CHOICES = [
        ('simple', 'Simple User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='admin')
    email = models.EmailField(unique=True)
    is_verified=models.BooleanField(default=False)
    
    objects=CustomUserManager()
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

# class SimpleUser(CustomUser):
#     objects=SimpleUserManager()
    


    

# class ModeratorUser(CustomUser):
#     pass

# class AdminUser(CustomUser):
#     pass
    

class OneTimePassword(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)
    code=models.CharField(max_length=6,unique=True)
    def __str__(self):
        return f"{self.user.username} passcode "
    