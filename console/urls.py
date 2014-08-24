from django.conf.urls import patterns, url
from .views import HomeView, FeedsView, WordsView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^feeds/$', FeedsView.as_view(), name='feeds'),
    url(r'^words/$', WordsView.as_view(), name='words'),
)
