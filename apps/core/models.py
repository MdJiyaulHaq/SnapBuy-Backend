from django.contrib.auth.models import AbstractUser, Group as BaseGroup
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)


class Group(BaseGroup):
    pass

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name

