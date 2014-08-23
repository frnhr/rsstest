from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from rest_framework_extensions.routers import ExtendedDefaultRouter


admin.autodiscover()


router = ExtendedDefaultRouter()
(
    router.register(r'feeds',
                    views.FeedViewSet,
                    base_name='feed')
          .register(r'entries',
                    views.EntryViewSet,
                    base_name='feeds-entry',
                    parents_query_lookups=['feed', ])
          .register(r'words',
                    views.WordViewSet,
                    base_name='feeds-entries-word',
                    parents_query_lookups=['entry__feed', 'entry', ])
)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
