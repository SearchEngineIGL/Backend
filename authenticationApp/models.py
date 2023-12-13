from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('simple', 'Simple User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='simple')
    email = models.EmailField(unique=True)
    
    objects=CustomUserManager()
    def __str__(self) :
        return self.email
    
    def tokens(self):
        pass
    

class SimpleUser(CustomUser):
    pass

    

class ModeratorUser(CustomUser):
    pass

class AdminUser(CustomUser):
    pass
    

class OneTimePassword(models.Model):
    user=models.OneToOneField(SimpleUser,on_delete=models.CASCADE)
    code=models.CharField(max_length=6,unique=True)
    def __str__(self):
        return f"{self.user.username} passcode "
    