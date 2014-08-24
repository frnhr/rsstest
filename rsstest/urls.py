from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', include('api.urls', app_name='api')),
    url(r'^console/', include('console.urls', app_name='console')),

    url(r'^admin/', include(admin.site.urls)),
)
