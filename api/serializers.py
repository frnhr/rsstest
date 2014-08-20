from rest_framework import serializers
from api.models import Feed, Entry, Word


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('_url', 'url', 'is_active', )


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('_url', 'feed', 'title', 'timestamp', 'text', )


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ('_url', 'word', 'count', 'entry', )