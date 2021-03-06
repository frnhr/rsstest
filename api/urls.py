from django.conf.urls import patterns, include, url
from rest_framework.routers import SimpleRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter
from . import views

router = ExtendedDefaultRouter()
(
    router.register(r'wordcounts', views.WordCountRootViewSet),
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
    router.register(r'words', views.WordCountTopViewSet, base_name='words-top'),
)


additional_router = SimpleRouter()
additional_router.register(r'wordcounts/simple', views.WordCountSimpleViewSet, base_name='wordcounts-simple'),
additional_router.register(r'wordcounts/json', views.WordCountSimpleJsonViewSet, base_name='wordcounts-json'),


urlpatterns = patterns('',
    url(r'', include(additional_router.urls)),
    url(r'', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
