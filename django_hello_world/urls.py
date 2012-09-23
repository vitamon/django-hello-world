from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django_hello_world.hello.views.home', name='home'),
    url(r'^edit/$', 'django_hello_world.hello.views.edit', name='edit'),
    url(r'^requests/$', 'django_hello_world.hello.views.requests', name='requests'),
    url(r'^logout/$', 'django_hello_world.hello.views.logout_view', name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name="login"),
    # url(r'^logout/$', 'django.contrib.auth.views.logout',{'template_name': 'logout.html' }, name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$'%settings.MEDIA_URL, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT,
          'show_indexes': True}),
    )