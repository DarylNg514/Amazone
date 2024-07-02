from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
