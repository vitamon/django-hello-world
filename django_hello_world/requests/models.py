from django.db import models
from django.core.cache import cache

# --------------------------------------------------------------
#
# RequestsLog model
#
# --------------------------------------------------------------
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
        verbose_name = "Request Priority"
        verbose_name_plural = "Request Priorities"
