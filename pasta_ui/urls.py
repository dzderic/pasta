from django.conf.urls import patterns, include, url

urlpatterns = patterns('pasta_ui.views',
    url(r'^$', 'home', name='home'),
)
