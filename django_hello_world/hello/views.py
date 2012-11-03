from django.http import HttpResponse
from django.utils import simplejson
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from hello.forms import  UserProfileForm
from hello.models import UserProfile
from django.contrib.auth import logout
from requests.models import RequestsLog, RequestsPriority
import settings
import time


@render_to('hello/home.html')
def home(request):
    if request.user.is_authenticated():
        return redirect(reverse("edit"))
    user = User.objects.all()[0]

    return {'profile': UserProfile.objects.get_or_create(user=user)[0],
            'is_authenticated': False}


@login_required
@render_to('hello/home_edit.html')
def edit(request):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    status, message = False, "Error"

    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=profile, files=request.FILES)

        if form.is_valid():
            if settings.DEBUG:
                time.sleep(1)# slow down a bit to check progress etc

            form.save()
            status, message = True, "Data was saved successfully"
        else:
            status, message = False, form.error_message_list()
    else:
        form = UserProfileForm(instance=profile)

    if request.is_ajax():
        return HttpResponse(simplejson.dumps({
            'status': status,
            'message': message,
        }), mimetype='application/javascript')
    else:
        return {'profile': profile,
                'is_authenticated': request.user.is_authenticated(),
                'form': form,
                'form_saved': status}


@render_to('hello/requests.html')
def requests(request):
    return {"items": RequestsLog.objects.get_last_10_sorted()}


def requests_up(request, id):
    RequestsPriority.objects.update_priority(id, 1)
    return redirect(reverse("requests"))


def requests_down(request, id):
    RequestsPriority.objects.update_priority(id, -1)
    return redirect(reverse("requests"))


def logout_view(request):
    logout(request)
    return redirect(reverse("home"))
