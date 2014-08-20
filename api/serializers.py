from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField, HyperlinkedRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer
from api.models import Feed, Entry, Word


# list serializers


class FeedListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('_url', 'url', 'is_active', )


class EntryListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('_url', 'title', )


class WordEntrySerializer(serializers.HyperlinkedModelSerializer):
    #_url = HyperlinkedIdentityField(view_name="word-detail", format='html', )
    
    class Meta:
        model = Word
        fields = ('_url', 'word', 'count', )



# detail serializers


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    entries = EntryListSerializer(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = ('_url', 'url', 'is_active', 'entries', )


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('_url', 'feed', 'title', 'timestamp', 'text', )


class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ('_url', 'word', 'count', 'entry', )

