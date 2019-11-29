from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ip = models.GenericIPAddressField(blank=True, null=True)
