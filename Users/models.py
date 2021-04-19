from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    uuid = models.CharField(max_length=36, blank=True)
    group = models.CharField(max_length=36, blank=True)

