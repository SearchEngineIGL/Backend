from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('simple', 'Simple User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='simple')
    #email = models.EmailField(max_length=100)
    

    #full_name = models.CharField(max_length=100)
    

class SimpleUser(CustomUser):
    @classmethod
    def create_user(cls,username,email,password):
        user=cls(username=username,email=email)
        user.set_password(password)
        user.save()
        return user


    

class ModeratorUser(CustomUser):
    @classmethod
    def create_user(cls,username,email,password):
        user=cls(username=username,email=email)
        user.set_password(password)
        user.save()
        return user


class AdminUser(CustomUser):
    @classmethod
    def create_user(cls,username,email,password):
        user=cls(username=username,email=email)
        user.set_password(password)
        user.save()
        return user

    
    