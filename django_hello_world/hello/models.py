from unittest import TestCase
import datetime
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.db.models.signals import post_save
import settings


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
    # This field is required.
    user = models.OneToOneField(User, related_name='profile')

    # Other fields here
    birthdate = models.DateField(blank=True, default=None, null=True)
    photo = models.ImageField(upload_to="photos/", default=None, null=True)

    jabber = models.CharField(max_length=20, default="", null=True)
    skype = models.CharField(max_length=20, default="", null=True)
    other_contacts = models.CharField(max_length=250, default="", null=True)
    bio = models.CharField(max_length=300, default="", null=True)

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
        self.user.last_name  = data["last_name"]
        self.user.email = data["email"]
        self.bio = data["bio"]
        self.jabber  = data["jabber"]
        self.photo = data["photo"]
        self.birthdate = data["birthdate"]
        self.skype = data["skype"]
        self.other_contacts = data["other_contacts"]

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

# --------------------------------------------------------------
#
# Models tests
#
# --------------------------------------------------------------
class ModelTest(TestCase):
    def test_add_item(self):
        time = datetime.datetime.now()
        item = RequestsLog(url="test1", time=time)
        item.save()
        saved_item = RequestsLog.objects.get_last_n(1)[0]
        assert saved_item.url == item.url

