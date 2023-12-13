from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=23)
    last_name = models.CharField(max_length=23)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=23)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

