from django.conf.urls import patterns, include, url
from .views import HomeView, FeedsView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^feeds/$', FeedsView.as_view(), name='feeds'),
)
