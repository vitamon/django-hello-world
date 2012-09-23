from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import Form
from django.views.decorators.csrf import csrf_exempt
import os
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from hello.forms import  UserProfileForm
from hello.models import RequestsLog
from django.contrib.auth import logout
from hello.util.modelUtils import unique_filename
import settings

@render_to('hello/home.html')
def home(request):
    if request.user.is_authenticated():
        return redirect(reverse("edit"))
    else:
        user = User.objects.all()[0]

    return {'user': user.get_profile().as_dict() if user else {},
            'photo': user.get_profile().photo,
            'is_authenticated': request.user.is_authenticated(),
    }


@login_required
@render_to('hello/home_edit.html')
def edit(request):
    user = request.user
    profile = request.user.get_profile()
    form_saved = False

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
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

    return {'photo': user.get_profile().photo,
            'is_authenticated': request.user.is_authenticated(),
            'form': form,
            'form_saved': form_saved}


@render_to('hello/requests.html')
def requests(request):
    top_ten = RequestsLog.objects.get_last_ten()
    return {"items": top_ten}


def logout_view(request):
    logout(request)
    return redirect(reverse("home"))


def upload_path(filename):
    return os.path.join(settings.MEDIA_ROOT, filename)

def handle_uploaded_file(f, filename):
    destination = open(upload_path(filename), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)