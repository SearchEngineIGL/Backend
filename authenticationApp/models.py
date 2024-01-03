from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
import json





class CustomUser(AbstractUser):
    
    USER_TYPE_CHOICES = [
        ('simple', 'Simple User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='admin')
    email = models.EmailField(unique=True)
    FullName= models.CharField(max_length=50, null=True, blank=True)
    PhoneNumber=models.CharField(max_length=20,null=True,blank=True)
    is_verified=models.BooleanField(default=False)
    photo= models.ImageField(upload_to='profile_pictures/',  null=True,blank=True)
    objects=CustomUserManager()
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    additional_data = models.JSONField(blank=True, null=True)

    def set_additional_data(self, data):
        self.additional_data = json.dumps(data)

    def get_additional_data(self):
        return json.loads(self.additional_data) if self.additional_data else {}
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
    