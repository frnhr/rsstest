from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from . import views


admin.autodiscover()


router = routers.DefaultRouter()
router.register(r'feeds', views.FeedViewSet)
router.register(r'entries', views.EntryViewSet)
router.register(r'words', views.WordViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
