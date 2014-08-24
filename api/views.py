from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin
from api.models import Feed, Entry, Word, WordCount
from .serializers import FeedListSerializer, EntryListSerializer, EntrySerializer, WordCountSerializer, FeedSerializer, \
    WordSerializer, WordCountListSerializer, WordListSerializer


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


class WordViewSet(DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows words in an entry to be viewed or edited.
    """
    http_method_names = ('get', 'head', 'options', )
    queryset = Word.objects.all()
    serializer_class = WordListSerializer
    serializer_detail_class = WordSerializer
