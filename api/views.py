from rest_framework import viewsets
from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin
from api.models import Feed, Entry, Word
from api.serializers import WordEntrySerializer
from .serializers import FeedListSerializer, EntryListSerializer, EntrySerializer, WordSerializer, FeedSerializer


class FeedViewSet(DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows feeds to be viewed or edited.
    """
    queryset = Feed.objects.all()
    serializer_class = FeedListSerializer
    serializer_detail_class = FeedSerializer


class EntryViewSet(DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows feed entries to be viewed or edited.
    """
    queryset = Entry.objects.all()
    serializer_class = EntryListSerializer
    serializer_detail_class = EntrySerializer
        

class WordViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows words in an entry to be viewed or edited.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer
