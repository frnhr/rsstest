from django.db.models import Sum
from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin
from api.models import Feed, Entry, Word, WordCount
from .serializers import FeedListSerializer, EntryListSerializer, EntrySerializer, WordCountSerializer, FeedSerializer, \
    WordCountListSerializer, WordListSerializer, WordCountRootSerializer


class FeedViewSet(DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows feeds to be viewed or edited.
    """
    queryset = Feed.objects.all()
    serializer_class = FeedListSerializer
    serializer_detail_class = FeedSerializer
    http_method_names = ('get', 'head', 'options', 'post', 'put', 'delete', )


class EntryViewSet(DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows feed entries to be viewed or edited.
    """
    http_method_names = ('get', 'head', 'options', )
    queryset = Entry.objects.all()
    serializer_class = EntryListSerializer
    serializer_detail_class = EntrySerializer


class WordCountViewSet(DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows words in an entry to be viewed or edited.
    """
    http_method_names = ('get', 'head', 'options', )
    queryset = WordCount.objects.all().order_by('-count')
    serializer_class = WordCountListSerializer
    serializer_detail_class = WordCountSerializer


class WordCountRootViewSet(DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows words in an entry to be viewed or edited.
    """
    http_method_names = ('get', 'head', 'options', )
    queryset = WordCount.objects.all()
    serializer_class = WordCountRootSerializer
    serializer_detail_class = WordCountRootSerializer

    def get_queryset(self, is_for_detail=False):
        queryset = super(WordCountRootViewSet, self).get_queryset(is_for_detail)
        if not is_for_detail:
            q = self.request.GET.get('q', None)
            if q:
                queryset = queryset.filter(word__word=q)
            f = self.request.GET.get('f', None)
            if f:
                queryset = queryset.filter(entry__feed__id=int(f)).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        response = super(WordCountRootViewSet, self).list(request, *args, **kwargs)
        response.data.insert(3, 'count__sum', self.get_queryset().aggregate(Sum('count'))['count__sum'])
        return response