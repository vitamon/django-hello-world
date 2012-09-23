import os
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from hello.forms import UploadImageForm, UserProfileForm
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

    return {'user': user.get_profile().as_dict() if user else {}, 'is_authenticated': request.user.is_authenticated()}


@login_required
@render_to('hello/home_edit.html')
def edit(request):
    user = request.user
    if request.method == 'POST': # If the form has been submitted...
        form = UserProfileForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            return redirect(reverse("home"))
    else:
        form = UserProfileForm(user.get_profile().as_dict()) # An unbound form

    return {'user': user.get_profile().as_dict(),
            'is_authenticated': request.user.is_authenticated(),
            'form': form }


@render_to('hello/requests.html')
def requests(request):
    top_ten = RequestsLog.objects.get_last_ten()
    return {"items": top_ten}


def logout_view(request):
    logout(request)
    return redirect(reverse("home"))


@login_required
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            #TODO add flash message

    return redirect(reverse("home"))


def handle_uploaded_file(f, filename):
    destination = open(os.path.join(settings.MEDIA_ROOT, filename), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)