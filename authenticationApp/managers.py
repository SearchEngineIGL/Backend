from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password



class CustomUserManager(BaseUserManager):
    def email_validator(self,email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("please enter a valid email adress"))
    
    def create_superuser(self,username,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_verified",True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is staff must be true for admin user"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is superuser must be true for admin user"))
        user_type="admin"
        user=self.create_user(
            username,email,password,user_type,**extra_fields
        )
        user.save()
        
        return user
    
    def authenticate_user(self, email, password):
        try:
            user = self.model.objects.get(email=email)
            # Check if the provided password is valid
            if check_password(password, user.password):
                return user
            else:
                return None
        except self.model.DoesNotExist:
            return None
        
    def create_user(self,username,email,password,user_type,**extra_fields):
            if email:
                email=self.normalize_email(email)
                self.email_validator(email)
            else:
                raise ValueError(_("an email adress is required"))
            user=self.model(username=username,email=email,user_type=user_type,**extra_fields)
            user.set_password(password)
            user.save()
            
            return user

    
        
# class SimpleUserManager(BaseUserManager):
#     def authenticate_user(self, email, password):
#         try:
#             user = self.model.objects.get(email=email)
#             # Check if the provided password is valid
#             if check_password(password, user.password):
#                 return user
#             else:
#                 return None
#         except self.model.DoesNotExist:
#             return None
#     def email_validator(self,email):
#         try:
#             validate_email(email)
#         except ValidationError:
#             raise ValueError(_("please enter a valid email adress"))
#     def create_user(self,username,email,password):
#             if email:
#                 email=self.normalize_email(email)
#                 self.email_validator(email)
#             else:
#                 raise ValueError(_("an email adress is required"))
#             user=self.model(username=username,email=email,user_type="simple")
#             user.set_password(password)
#             user.save()
#             return user