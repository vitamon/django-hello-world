from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django_hello_world.hello.views.home', name='home'),
    url(r'^edit/$', 'django_hello_world.hello.views.edit', name='edit'),
    url(r'^requests/$', 'django_hello_world.hello.views.requests', name='requests'),
    url(r'^requests/up/(?P<id>\d+)/$', 'django_hello_world.hello.views.requests_up', name='req_up'),
    url(r'^requests/down/(?P<id>\d+)/$', 'django_hello_world.hello.views.requests_down', name='req_down'),
    url(r'^logout/$', 'django_hello_world.hello.views.logout_view', name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name="login"),
    # url(r'^logout/$', 'django.contrib.auth.views.logout',{'template_name': 'logout.html' }, name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# for callendar widget
urlpatterns += patterns('',
    (r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$'%settings.MEDIA_URL, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT,
          'show_indexes': True}),
    )

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)