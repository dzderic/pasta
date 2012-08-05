from django.conf.urls import patterns, include, url

urlpatterns = patterns('pasta_app.views',
    url(r'^$', 'home', name='home'),
    url(r'^new/$', 'new_pasta', name='new-pasta'),
    url(r'^([^/]+)/([^/]+)$', 'edit_pasta', name='edit-pasta'),
)
