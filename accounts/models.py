from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    pass  
class CustomUser(AbstractUser):
    class Meta:
        app_label = 'accounts'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)

    objects = CustomUserManager()

CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'
