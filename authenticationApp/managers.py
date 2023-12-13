from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validator(self,email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("please enter a valid email adress"))

    def create_user(self,username,email,password):
            if email:
                email=self.normalize_email(email)
                self.email_validator(email)
            else:
                raise ValueError(_("an email adress is required"))
            user=self.model(username=username,email=email)
            user.set_password(password)
            user.save()
            return user
