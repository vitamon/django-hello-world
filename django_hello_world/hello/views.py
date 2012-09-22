from annoying.decorators import render_to
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from hello.models import RequestsLog

@render_to('hello/home.html')
def home(request):
    return {}


@render_to('hello/requests.html')
def requests(request):
    top_ten = RequestsLog.objects.get_last_ten()
    return {"items": top_ten}


def login(request):
    return {}

class AuthenticationView(FormView):
    template_name = "registration/login.html"
    form_class = AuthenticationForm

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AuthenticationView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.kwargs.get("next", reverse('home'))

    def get(self, request, *args, **kwargs):
        if request.GET.has_key('authcode'):
            return self.post(request, *args, **kwargs)
        return super(AuthenticationView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
                })
        if self.request.method == 'GET' and self.request.GET.has_key('authcode'):
            kwargs.update({
                'data': self.request.GET
            })
        return kwargs

    def form_valid(self, form):
        if hasattr(form, 'clubcard_newuser') and form.clubcard_newuser:
            self.kwargs.update({
                'next': reverse('accounts_register_clubcard')
            })
            self.request.session[CARD_ID_SESSION_KEY] = form.cleaned_data['authcode']
            return super(AuthenticationView, self).form_valid(form)

        login(self.request, form.get_user())
        return super(AuthenticationView, self).form_valid(form)
