from django.db import models
from django.contrib.auth.models import AbstractUser
from boards.models import Entity

# Create your models here.
class User(AbstractUser):
    entity = models.ForeignKey(Entity, on_delete = models.PROTECT, related_name = 'User', blank = True, null = True)