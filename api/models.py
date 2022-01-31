from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from datetime import datetime

from django.db.models.signals import post_save


# Create your models here.


"""
Dublin Core
Contributor – "An entity responsible for making contributions to the resource".
Coverage – "The spatial or temporal topic of the resource, the spatial applicability of the resource, or the jurisdiction under which the resource is relevant".
Creator – "An entity primarily responsible for making the resource".
Date – "A point or period of time associated with an event in the lifecycle of the resource".
Description – "An account of the resource".
Format – "The file format, physical medium, or dimensions of the resource".
Identifier – "An unambiguous reference to the resource within a given context".
Language – "A language of the resource".
Publisher – "An entity responsible for making the resource available".
Relation – "A related resource".
Rights – "Information about rights held in and over the resource".
Source – "A related resource from which the described resource is derived".
Subject – "The topic of the resource".
Title – "A name given to the resource".
Type – "The nature or genre of the resource".
"""

from .managers import CustomUserManager


class OvaUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    cedula = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # 'username', 'email', 'first_name', 'last_name', 'cedula'

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Ova(models.Model):
    contributor = models.CharField(max_length=255)
    coverage = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now())
    description = models.TextField()
    format = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)
    rights = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    source = models.TextField()
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    link = models.FileField(upload_to='ovas/')

    def __str__(self):
        return self.title


class Score(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    ova_id = models.ForeignKey(Ova, on_delete=models.DO_NOTHING)
    score = models.IntegerField()


class UserSubject(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.pk


def notify_users_per_ova(sender, instance, **kwargs):
    from fcm_django.models import FCMDevice
    subject_to_send = instance.subject
    subjects = UserSubject.objects.filter(subject_id=subject_to_send).values('user_id')
    lista_ids = [item['user_id'] for item in subjects]

    dispositivos = FCMDevice.objects.filter(user__in=lista_ids, active=True)
    dispositivos.send_message(
        message="",
        title="Ova Nueva Disponible",
        body="",
        icon=""
    )
    print("llegue al final")


post_save.connect(notify_users_per_ova, sender=Ova)
