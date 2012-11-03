from annoying.decorators import render_to
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from requests.models import RequestsPriority, RequestsLog

@render_to('hello/requests.html')
def requests(request):
    return {"items": RequestsLog.objects.get_last_10_sorted()}


def requests_up(request, id):
    RequestsPriority.objects.update_priority(id, 1)
    return redirect(reverse("requests"))


def requests_down(request, id):
    RequestsPriority.objects.update_priority(id, -1)
    return redirect(reverse("requests"))
