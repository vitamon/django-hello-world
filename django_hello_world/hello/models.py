import datetime
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache


# --------------------------------------------------------------
#
# RequestsLog model
#
# --------------------------------------------------------------
from django.dispatch import receiver
from django.forms import model_to_dict

class RequestsLogManager(models.Manager):
    def get_last_ten(self):
        return self.get_last_n(10)

    def get_last_n(self, n):
        return list(self.order_by("-time")[:n])

    def get_last_10_sorted(self):
        sorted = []
        for item in self.get_last_ten():
            obj = model_to_dict(item)
            obj['priority'] = RequestsPriority.objects.lookup(url=item.url)
            sorted.append(obj)
        sorted.sort(key=lambda obj: obj['priority'], reverse=True)
        return sorted


class RequestsLog(models.Model):
    url = models.URLField()
    time = models.DateTimeField()

    objects = RequestsLogManager()

    class Meta:
        db_table = 'request_log'

# --------------------------------------------------------------
#
# RequestsPriority model
#
# --------------------------------------------------------------

class RequestsPriorityManager(models.Manager):
    DEFAULT_PRIORITY = 0

    def lookup(self, url):
        cached_priority = cache.get(url)
        if cached_priority is not None:
            #print "cache hit! ", url, cached_priority
            return cached_priority
        try:
            item = self.get(url=url)
            cache.set(url, item.priority)
            return item.priority
        except:
            cache.set(url, self.DEFAULT_PRIORITY)
            return self.DEFAULT_PRIORITY


    def update_priority(self, id, delta):
        item, created = RequestsPriority.objects.get_or_create(url=RequestsLog.objects.get(id=id).url)
        item.priority += delta
        item.save()
        cache.set(item.url, item.priority)


class RequestsPriority(models.Model):
    url = models.URLField()
    priority = models.SmallIntegerField(default=0)

    objects = RequestsPriorityManager()

    class Meta:
        db_table = 'hello_request_priority'

# --------------------------------------------------------------
#
# User profile model
#
# --------------------------------------------------------------

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    birthdate = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    jabber = models.CharField(max_length=20, blank=True, null=True)
    skype = models.CharField(max_length=20, blank=True, null=True)
    other_contacts = models.CharField(max_length=250, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)

    @staticmethod
    def ensure_profile_for(user):
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            profile.save()
        return profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.ensure_profile_for(instance)

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



