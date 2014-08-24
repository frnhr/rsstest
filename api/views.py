from django.db.models import Sum
from django.http.response import HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import is_client_error
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin
from api.models import Feed, Entry, Word, WordCount
from .serializers import FeedListSerializer, EntryListSerializer, EntrySerializer, WordCountSerializer, FeedSerializer, \
    WordCountListSerializer, WordListSerializer, WordCountRootSerializer


# noinspection PyUnresolvedReferences
class RenameResultsCountMixin(object):
    """
    Renames "count" field on ListView views to "results_count", so that it is not confused with word counts.
    """
    def list(self, request, *args, **kwargs):
        response = super(RenameResultsCountMixin, self).list(request, *args, **kwargs)
        results_count = response.data['count']
        index = response.data.keys().index('count')
        del response.data['count']
        response.data.insert(index, 'results_count', results_count)
        return response


class FeedViewSet(RenameResultsCountMixin, DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows feeds to be viewed or edited.
    """
    queryset = Feed.objects.all()
    serializer_class = FeedListSerializer
    serializer_detail_class = FeedSerializer
    http_method_names = ('get', 'head', 'options', 'post', 'put', 'delete', )


class EntryViewSet(RenameResultsCountMixin, DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows feed entries to be viewed or edited.
    """
    http_method_names = ('get', 'head', 'options', )
    queryset = Entry.objects.all()
    serializer_class = EntryListSerializer
    serializer_detail_class = EntrySerializer


class WordCountViewSet(RenameResultsCountMixin, DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows words in an entry to be viewed or edited.
    """
    http_method_names = ('get', 'head', 'options', )
    queryset = WordCount.objects.all().order_by('-count')
    serializer_class = WordCountListSerializer
    serializer_detail_class = WordCountSerializer


class WordCountRootViewSet(RenameResultsCountMixin, DetailSerializerMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows words in an entry to be viewed or edited.
    """
    http_method_names = ('get', 'head', 'options', )
    queryset = WordCount.objects.all()
    serializer_class = WordCountRootSerializer
    serializer_detail_class = WordCountRootSerializer

    status = 200
    message = ''

    def get_queryset(self, is_for_detail=False):
        queryset = super(WordCountRootViewSet, self).get_queryset(is_for_detail)
        if not is_for_detail:
            q = self.request.GET.get('q', None)
            if q:
                queryset = queryset.filter(word__word=q)
            f = self.request.GET.get('f', None)  # url decoded behind-the-scene
            e = self.request.GET.get('e', None)  # url decoded behind-the-scene
            if f and e:
                #@TODO this self.stuff thing is not the prettiest way of accomplishing this.
                # perhaps move this check to list()
                # it tests thread-safe though
                self.status = status.HTTP_406_NOT_ACCEPTABLE
                self.message = u'Please use either "f" or "e" query, bot not both.'
            
            if f:
                try:
                    f_int = int(f)
                except ValueError:
                    f_int = False
                if f_int and str(f_int) == f:  # ?f=<id>
                    queryset = queryset.filter(entry__feed__id=f_int).distinct()
                else:  # ?f=<url>
                    queryset = queryset.filter(entry__feed__url=f).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        response = super(WordCountRootViewSet, self).list(request, *args, **kwargs)
        if is_client_error(self.status):
            return Response(self.message, status=self.status)
        response.data.insert(3, 'count__sum', self.get_queryset().aggregate(Sum('count'))['count__sum'])
        return response
