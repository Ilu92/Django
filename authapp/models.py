from datetime import timedelta

from Tools.demo.mcast import receiver
from django.db.models.signals import post_save
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

    gender = models.CharField(
        verbose_name='пол',
        max_length=1,
        choices=GENDER_CHOISES,
        blank=True
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()