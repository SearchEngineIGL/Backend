from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
import json


"""_summary_
    Manager class to validate user account or admin account 

    Returns:
        _User_: _return a validate account for user , admin_
    """
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
        user.set_additional_data({'list_of_moderators':[]})
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
            if user_type=="simple":
                #on crée une liste des favoris pour l'utilisateur simple
                user.set_additional_data({'list_of_favorites':[]})
            elif user_type=="moderator":
                #On ajoute le moderateur à la liste des moderateurs de l'admin ...
                admin_user=self.get(user_type="admin")
                list_of_moderators = admin_user.get_additional_data().get('list_of_moderators', [])
                user_dict = {'username': user.username, 'email': user.email, 'user_type': user.user_type,'password':password}
                list_of_moderators.append(user_dict)
                #serialized_list = [json.dumps(obj) for obj in list_of_moderators]
                admin_user.set_additional_data({'list_of_moderators': list_of_moderators})
                admin_user.save()
            user.save()
            
            return user
    def create_moderator_user(self,username,email,user_type,**extra_fields):
        user_type="moderator"
        #by default, the password is the username
        password=username
        user=self.create_user(
            username,email,password,user_type,**extra_fields
        )
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