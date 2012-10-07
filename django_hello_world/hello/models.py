import datetime
from django.db import models
from django.db.models.signals import post_save, post_delete


# --------------------------------------------------------------
#
# RequestsLog model
#
# --------------------------------------------------------------
from django.dispatch import receiver, Signal

class RequestsLogManager(models.Manager):
    def get_last_ten(self):
        return self.get_last_n(10)

    def get_last_n(self, n):
        return self.order_by("-time")[:n]


class RequestsLog(models.Model):
    url = models.URLField()
    time = models.DateTimeField()
    objects = RequestsLogManager()

    class Meta:
        db_table = 'request_log'


# --------------------------------------------------------------
#
# User profile model
#
# --------------------------------------------------------------

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    # Other fields here
    birthdate = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)

    jabber = models.CharField(max_length=20, blank=True, null=True)
    skype = models.CharField(max_length=20, blank=True, null=True)
    other_contacts = models.CharField(max_length=250, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)

    def as_dict(self):
        return {
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "bio": self.bio,
            "jabber": self.jabber,
            "photo": self.photo,
            "birthdate": self.birthdate,
            "skype": self.skype,
            "other_contacts": self.other_contacts
        }

    def update_from(self, data):
        self.user.first_name = data["first_name"]
        self.user.last_name = data["last_name"]
        self.user.email = data["email"]
        self.bio = data["bio"]
        self.jabber = data["jabber"]
        self.photo = data["photo"]
        self.birthdate = data["birthdate"]
        self.skype = data["skype"]
        self.other_contacts = data["other_contacts"]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, profile_created = UserProfile.objects.get_or_create(user=instance)
        if profile_created:
            profile.save()

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
        default=ADDED)
    time = models.DateTimeField()

    class Meta:
        db_table = 'creation_log'


@receiver(post_save, sender=None)
def all_creations_logger(sender, instance, created, **kwargs):
    if not (type(instance) is CreationLog):
        #print "save", sender, created
        item = CreationLog(class_name=str(sender), operation=CreationLog.ADDED if created else CreationLog.UPDATED,
            time=datetime.datetime.now())
        item.save()


@receiver(post_delete, sender=None)
def all_deletions_logger(sender, instance, **kwargs):
    #print "del", sender
    item = CreationLog(class_name=str(sender), operation=CreationLog.DELETED, time=datetime.datetime.now())
    item.save()



