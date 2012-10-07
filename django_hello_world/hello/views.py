import os
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response, render
from hello.forms import  UserProfileForm
from hello.models import RequestsLog, UserProfile, RequestsPriority
from django.contrib.auth import logout
from hello.util.modelUtils import unique_filename
import settings

@render_to('hello/home.html')
def home(request):
    if request.user.is_authenticated():
        return redirect(reverse("edit"))
    else:
        user = User.objects.all()[0]

    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        profile.save()

    return {'user': profile.as_dict() if user else {},
            'photo':profile.photo,
            'is_authenticated': False,
    }


@login_required
@render_to('hello/home_edit.html')
def edit(request):
    user = request.user
    profile = user.get_profile()
    form_saved = False
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():

            # slow down a bit to check progress etc
            if settings.DEBUG:
                import time
                time.sleep(1)

            photoFileName = profile.photo

            if request.FILES and 'photo' in request.FILES:
                photoFileName = unique_filename(request.FILES['photo']._name)
                handle_uploaded_file(request.FILES['photo'], photoFileName)

            profile.update_from(form.cleaned_data)
            profile.photo = photoFileName
            profile.save()
            user.save()
            form_saved = True
        else:
            print form.errors
    else:
        form = UserProfileForm(user.get_profile().as_dict())

    if request.is_ajax():
        return render_to_response('hello/photo_result.html',
            {'photo': user.get_profile().photo,
             'settings':settings,
             'form_saved': form_saved})
    else:
        return {'photo': user.get_profile().photo,
                'is_authenticated': request.user.is_authenticated(),
                'form': form,
                'form_saved': form_saved}


@render_to('hello/requests.html')
def requests(request):
    top_ten = RequestsLog.objects.get_last_ten()
    return {"items": top_ten}

@render_to('hello/requests.html')
def requests_up(request, id):
    RequestsPriority.objects.update_priority(id, 1)
    return redirect(reverse("requests"))


@render_to('hello/requests.html')
def requests_down(request, id):
    RequestsPriority.objects.update_priority(id, -1)
    return redirect(reverse("requests"))


def logout_view(request):
    logout(request)
    return redirect(reverse("home"))


def upload_path(filename):
    return os.path.join(settings.MEDIA_ROOT, filename)


def handle_uploaded_file(f, filename):
    destination = open(upload_path(filename), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)