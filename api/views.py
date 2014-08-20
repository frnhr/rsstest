from rest_framework import viewsets
from api.models import Feed, Entry, Word
from .serializers import FeedSerializer, EntrySerializer, WordSerializer


class FeedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows feeds to be viewed or edited.
    """
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    

class EntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows feed entries to be viewed or edited.
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class WordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows words in an entry to be viewed or edited.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer
