from annoying.decorators import render_to
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from hello.models import RequestsLog
from django.contrib.auth import logout

@render_to('hello/home.html')
def home(request):
    return {'user':request.user}


@render_to('hello/requests.html')
def requests(request):
    top_ten = RequestsLog.objects.get_last_ten()
    return {"items": top_ten}

def logout_view(request):
    logout(request)
    return redirect(reverse("home"))
