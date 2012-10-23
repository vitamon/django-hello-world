from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'django_hello_world.requests.views.requests', name='requests'),
    url(r'^up/(?P<id>\d+)/$', 'django_hello_world.requests.views.requests_up', name='req_up'),
    url(r'^down/(?P<id>\d+)/$', 'django_hello_world.requests.views.requests_down', name='req_down'),
)
