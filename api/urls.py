from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter


admin.autodiscover()


additional_router = SimpleRouter()
additional_router.register(r'words/simple', views.WordCountSimpleViewSet, base_name='words-simple'),
additional_router.register(r'words/json', views.WordCountSimpleJsonViewSet, base_name='words-json'),


router = ExtendedDefaultRouter()
(
    router.register(r'words', views.WordCountRootViewSet),
    router.register(r'feeds',
                    views.FeedViewSet,
                    base_name='feed')
          .register(r'entries',
                    views.EntryViewSet,
                    base_name='feeds-entry',
                    parents_query_lookups=['feed', ])
          .register(r'wordcounts',
                    views.WordCountViewSet,
                    base_name='feeds-entries-wordcount',
                    parents_query_lookups=['entry__feed', 'entry', ]),
)

urlpatterns = patterns('',
    url(r'', include(additional_router.urls)),
    url(r'', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
