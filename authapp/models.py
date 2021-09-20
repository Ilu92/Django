from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.tamezone import now


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveIntegerFiels(verbose_name='возраст', blank=True, null=True)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expires(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOISES = (
        (MALE, 'М'),
        (FEMALE, 'Ж')
    )

    user = models.OneToOneField(
        User,
        unique=True,
        null=False,
        db_index=True,
        om_delete=models.CASCADE
    )

    tagline=models.CharField(
        verbose_name='теги',
        max_length=128,
        blank=True,
    )

    abotme = models.TextField(
        verbose_name='о себе',
        max_length=128,
        blank=True,
    )

