from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.relations import HyperlinkedIdentityField, HyperlinkedRelatedField
from rest_framework.reverse import reverse
from rest_framework.serializers import HyperlinkedModelSerializer, Serializer
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

class LinkNestedSelf(Field):
    url = None
    view_name = None
    lookup_parents = None
    url_parameters = None
    parent_fields = None
    field = None
    
    def __init__(self, view_name, lookup_parents, url_parameters=None, parent_fields=None, field='pk', *args, **kwargs):
        super(LinkNestedSelf, self).__init__(*args, **kwargs)
        self.view_name = view_name
        self.lookup_parents = lookup_parents
        self.url_parameters = url_parameters
        self.parent_fields = parent_fields
        self.field = field
        
    def field_to_native(self, obj, field_name):
        request = self.context.get('request', None)
        lookup_parents = self.lookup_parents[::-1]
        if self.url_parameters is None:
            self.url_parameters = ['pk'] * len(self.lookup_parents)
        url_parameters = self.url_parameters[::-1]
        if self.parent_fields is None:
            self.parent_fields = ['pk'] * len(self.lookup_parents)
        parent_fields = self.parent_fields[::-1]
        parents = []
        kwargs = {
            self.field: getattr(obj, self.field),
        }
        for field_name in lookup_parents:
            if "__" not in field_name:  #@TODO /me should have done a recursion, really...
                parents.append((getattr(obj, field_name), field_name))
            else:
                known_name, new_name = field_name.split("__", 1)
                parents.append((getattr(parents[-1][0], new_name), new_name))
        that = obj
        for i, (parent, field_name) in enumerate(parents):
            kwargs[url_parameters[i]] = getattr(getattr(that, field_name), parent_fields[i])
            that = parent
        return reverse(self.view_name, kwargs=kwargs, request=request)


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    entries = EntryListSerializer(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = ('_url', 'url', 'is_active', 'entries', )
        #view_name = "feed"


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('_url', 'feed', 'title', 'timestamp', 'text', )
        #view_name = "feeds-entry"


class WordSerializer(serializers.HyperlinkedModelSerializer):
    _url = LinkNestedSelf(view_name="feeds-entries-word-detail", lookup_parents=['entry__feed', 'entry', ], url_parameters=['parent_lookup_entry__feed', 'parent_lookup_entry'], parent_fields=['pk', 'pk'])
    
    class Meta:
        model = Word
        fields = ('_url', 'word', 'count', 'entry', )
        #view_name = "feeds-entries-word-detail"

