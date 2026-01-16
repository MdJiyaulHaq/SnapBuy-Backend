from django.contrib.auth.models import AbstractUser, Group as BaseGroup
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)


class Group(BaseGroup):
    """Proxy model to display Groups in the same admin section as Users"""

    class Meta:
        proxy = True
        verbose_name = "Group"
        verbose_name_plural = "Groups"

