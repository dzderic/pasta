from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login

from pasta_app.forms import BootstrapAuthForm

urlpatterns = patterns('pasta_app.views',
    url(r'^$', 'home', name='home'),
    url(r'^new/$', 'new_pasta', name='new-pasta'),
    url(r'^accounts/login/$', login, name='login',
        kwargs={'template_name': 'login.html', 'authentication_form': BootstrapAuthForm}),
    url(r'^accounts/logout/$', logout_then_login, name='logout'),

    # This should be last as it matches almost anything
    url(r'^(?P<owner>[^/]+)/(?P<slug>[^/]+)/(?:(?P<ref>[^/]+)/)?$', 'view_pasta', name='view-pasta'),
)
