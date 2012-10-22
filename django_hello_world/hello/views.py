from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response, render
from hello.forms import  UserProfileForm
from hello.models import RequestsLog, UserProfile, RequestsPriority
from django.contrib.auth import logout
from hello.util.utils import unique_filename, handle_uploaded_file
import settings
import time


@render_to('hello/home.html')
def home(request):
    if request.user.is_authenticated():
        return redirect(reverse("edit"))
    user = User.objects.all()[0]

    return {'profile': UserProfile.ensure_profile_for(user),
            'is_authenticated': False}


@login_required
@render_to('hello/home_edit.html')
def edit(request):
    profile = request.user.get_profile()
    form_saved = False
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=profile, files=request.FILES)

        if form.is_valid():
            # slow down a bit to check progress etc
            if settings.DEBUG:
                time.sleep(1)

            if request.FILES and 'photo' in request.FILES:
                photoFileName = unique_filename(request.FILES['photo']._name)
                handle_uploaded_file(request.FILES['photo'], photoFileName)
                profile.photo = photoFileName

            form.save()
            form_saved = True
        else:
            # TODO: change to ajax json
            print form.errors
    else:
        form = UserProfileForm(instance=profile)

    if request.is_ajax():
        return render_to_response('hello/photo_result.html',
            {'profile': profile,
             'settings': settings,
             'form_saved': form_saved})
    else:
        return {'profile': profile,
                'is_authenticated': request.user.is_authenticated(),
                'form': form,
                'form_saved': form_saved}


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
