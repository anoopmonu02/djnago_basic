from django.db import models
#from .manager import UserManager
#from django.contrib.auth.models import AbstractUser


# Create your models here.

""" class CustomUser(AbstractUser):  
    print("-------------------------------------------")
    username = None  
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    user_bio = models.CharField(max_length=100)
    user_comments = models.TextField(max_length=255, blank=True, null=True)
    user_profile_image = models.ImageField(upload_to='profile')
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [] """