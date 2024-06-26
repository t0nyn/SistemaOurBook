from django.db import models
from django.contrib.auth.models import AbstractUser


class OurBookUser(AbstractUser):
    cpf = models.CharField(max_length=14, primary_key=True)
