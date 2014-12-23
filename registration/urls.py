from django.conf.urls import patterns, include, url

urlpatterns = patterns('registration.views',
    url(r'^register/$', 'register_view', name='registration_register'),
    url(r'^login/$', 'login_view', name='registration_login'),
    url(r'^logout/$', 'logout_view', name='registration_logout'),
    url(r'^activation/(\w+)/$', 'activation_view', name='registration_activation'),
)