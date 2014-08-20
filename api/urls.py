from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from . import views
from rest_framework_extensions.routers import ExtendedSimpleRouter


admin.autodiscover()


router = routers.DefaultRouter()
router.register(r'feeds', views.FeedViewSet)
router.register(r'entries', views.EntryViewSet)
router.register(r'words', views.WordViewSet)

router2 = ExtendedSimpleRouter()
(
    router2.register(r'feeds',
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
#urlpatterns = router.urls

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^', include(router2.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
