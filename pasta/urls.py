from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('pasta_app.urls')),

    # Enable django admin
    url(r'^admin/', include(admin.site.urls)),
)
