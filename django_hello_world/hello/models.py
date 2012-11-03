import datetime
from django.db import models
from django.db.models.signals import post_save, post_delete

# --------------------------------------------------------------
#
# User profile model
#
# --------------------------------------------------------------

from django.contrib.auth.models import User
from django.dispatch import receiver
from hello.util.utils import get_image_path

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    birthdate = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    jabber = models.CharField(max_length=20, blank=True, null=True)
    skype = models.CharField(max_length=20, blank=True, null=True)
    other_contacts = models.CharField(max_length=250, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

# --------------------------------------------------------------
#
# Creation log model
#
# --------------------------------------------------------------

class CreationLog(models.Model):
    DELETED = 'DEL'
    ADDED = 'ADD'
    UPDATED = 'UPD'
    OPERATIONS = (
        (DELETED, 'Deleted'),
        (ADDED, 'Added'),
        (UPDATED, 'Updated'),
        )
    class_name = models.CharField(max_length=256, blank=False)
    operation = models.CharField(max_length=3,
        choices=OPERATIONS,
        default=ADDED, blank=False)
    time = models.DateTimeField()

    class Meta:
        db_table = 'creation_log'


@receiver(post_save, sender=None)
def all_creations_logger(sender, instance, created, **kwargs):
    if not isinstance(instance, CreationLog):
        CreationLog.objects.create(
            class_name=str(sender),
            operation=CreationLog.ADDED if created else CreationLog.UPDATED,
            time=datetime.datetime.now())


@receiver(post_delete, sender=None)
def all_deletions_logger(sender, instance, **kwargs):
    CreationLog.objects.create(class_name=str(sender), operation=CreationLog.DELETED, time=datetime.datetime.now())



