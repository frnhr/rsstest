from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.reverse import reverse
from api.models import Feed, Entry, Word, WordCount


class HyperlinkNestedSelf(Field):
    url = None
    view_name = None
    parents_lookup = None
    self_field = None
    obj_field = None

    def __init__(self, view_name, parents_lookup=None, obj_field=None, self_field='pk', *args, **kwargs):
        super(HyperlinkNestedSelf, self).__init__(*args, **kwargs)
        self.view_name = view_name
        self.parents_lookup = parents_lookup
        self.self_field = self_field
        self.obj_field = obj_field

    def field_to_native(self, obj, field_name):
        request = self.context.get('request', None)
        parents_lookup = [[parent_lookup, 'pk'] if isinstance(parent_lookup, basestring) else parent_lookup
                            for parent_lookup in self.parents_lookup]  # copy the list and make "pk" optional default
        if self.obj_field is not None:
            obj = getattr(obj, self.obj_field)
            #@TODO this is a good point to unify with HyperlinkNestedViewField

        def get_parent_data(parent_lookup, parent_data):
            """
            Gather parent objects and field values
            """
            if len(parent_lookup) < 1:
                return parent_data
            lookup = parent_lookup.pop()
            parent_attr = lookup[0].split("__")[-1] 
            parent_field = lookup[1]
            obj = parent_data[-1]['obj']
            parent = getattr(obj, parent_attr)
            parent_data.append({
                'obj': parent,
                'field': parent_field,
                'value': getattr(parent, parent_field),
                'lookup': lookup[0],
            })
            return get_parent_data(parent_lookup, parent_data)

        parent_data = [{'obj': obj, 'field': self.self_field, 'value': getattr(obj, self.self_field) }, ]
        parents_data = get_parent_data(parents_lookup, parent_data)
        
        kwargs = {}  # populate kwargs for URL reverse() call
        for i, parent_data in enumerate(parents_data):
            if i == 0:
                kwargs[parent_data['field']] = parent_data['value']
            else:
                kwargs['parent_lookup_%s' % parent_data['lookup']] = parent_data['value']
        
        return reverse(self.view_name, kwargs=kwargs, request=request)

#@TODO DRY it out
class HyperlinkNestedViewField(Field):
    url = None
    view_name = None
    parents_lookup = None
    nested_field = None
    
    def __init__(self, view_name, parents_lookup=None, nested_field=None, *args, **kwargs):
        super(HyperlinkNestedViewField, self).__init__(*args, **kwargs)
        self.view_name = view_name
        self.parents_lookup = parents_lookup
        self.nested_field = nested_field
        
    def field_to_native(self, obj, field_name):
        request = self.context.get('request', None)
        parents_lookup = [[parent_lookup, 'pk'] if isinstance(parent_lookup, basestring) else parent_lookup
                            for parent_lookup in self.parents_lookup]  # copy the list and make "pk" optional default
        
        def get_parent_data(parent_lookup, parent_data):
            """
            Gather parent objects and field values
            """
            if len(parent_lookup) < 1:
                return parent_data
            lookup = parent_lookup.pop()
            parent_attr = lookup[0].split("__")[-1] 
            parent_field = lookup[1]
            obj = parent_data[-1]['obj']
            parent = getattr(obj, parent_attr)
            parent_data.append({
                'obj': parent,
                'field': parent_field,
                'value': getattr(parent, parent_field),
                'lookup': lookup[0],
            })
            return get_parent_data(parent_lookup, parent_data)
        nested_obj = getattr(obj, self.nested_field).model()  #@TODO not a nice trick, creating a dummy nested object
        setattr(nested_obj, parents_lookup[-1][0], obj)
        parent_data = [{'obj': nested_obj, 'field': 'pk', 'value': getattr(nested_obj, 'pk') }, ]
        parents_data = get_parent_data(parents_lookup, parent_data)
        
        kwargs = {}  # populate kwargs for URL reverse() call
        for i, parent_data in enumerate(parents_data):
            if i == 0:
                pass
            else:
                kwargs['parent_lookup_%s' % parent_data['lookup']] = parent_data['value']
        
        return reverse(self.view_name, kwargs=kwargs, request=request)


# list serializers


class FeedListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('_url', 'url', 'is_active', )


class EntryListSerializer(serializers.HyperlinkedModelSerializer):
    _url = HyperlinkNestedSelf(view_name="feeds-entry-detail", parents_lookup=['feed', ])

    class Meta:
        model = Entry
        fields = ('_url', 'title', )


class WordEntrySerializer(serializers.HyperlinkedModelSerializer):
    #_url = HyperlinkedIdentityField(view_name="word-detail", format='html', )

    class Meta:
        model = Word
        fields = ('_url', 'word', 'count', )
        read_only_fields = fields


class WordField(serializers.CharField):

    def field_to_native(self, obj, field_name):
        """
        Given and object and a field name, returns the value that should be
        serialized for that field.
        """
        return obj.word.word


class WordCountListSerializer(serializers.HyperlinkedModelSerializer):
    _url = HyperlinkNestedSelf(view_name="feeds-entries-wordcount-detail", parents_lookup=['entry__feed', 'entry', ])
    word = WordField()

    class Meta:
        model = WordCount
        fields = ('_url', 'word', 'count', )

class WordCountWordListSerializer(serializers.HyperlinkedModelSerializer):
    _url = HyperlinkNestedSelf(view_name="feeds-entries-wordcount-detail", parents_lookup=['entry__feed', 'entry', ])
    entry = HyperlinkNestedSelf(view_name="feeds-entry-detail", parents_lookup=['feed', ], obj_field='entry')
    
    class Meta:
        model = WordCount
        fields = ('_url', 'entry', 'count', )


class WordListSerializer(serializers.HyperlinkedModelSerializer):
    wordcounts = WordCountWordListSerializer()
    
    class Meta:
        model = Word
        fields = ('_url', 'word', 'wordcounts', )



# detail serializers


class WordCountRootSerializer(serializers.HyperlinkedModelSerializer):

    class FeedURLField(Field):
        def field_to_native(self, obj, field_name):
            return obj.entry.feed.url
    
    class EntryTitleField(Field):
        def field_to_native(self, obj, field_name):
            return obj.entry.title
    
    _url = HyperlinkNestedSelf(view_name="feeds-entries-wordcount-detail", parents_lookup=['entry__feed', 'entry', ])
    word = WordField()
    entry = HyperlinkNestedSelf(view_name="feeds-entry-detail", parents_lookup=['feed', ], obj_field='entry')
    entry_title = EntryTitleField()
    feed_url = FeedURLField()
    


    class Meta:
        model = WordCount
        fields = ('_url', 'word', 'count', 'entry', 'entry_title', 'feed_url' )


class WordCountSerializer(serializers.HyperlinkedModelSerializer):
    _url = HyperlinkNestedSelf(view_name="feeds-entries-wordcount-detail", parents_lookup=['entry__feed', 'entry', ])
    entry = HyperlinkNestedSelf(view_name="feeds-entry-detail", parents_lookup=['feed', ], obj_field='entry')
    word = WordField()
    
    class Meta:
        model = WordCount
        fields = ('_url', 'entry', 'word', 'count', )


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    _url = HyperlinkNestedSelf(view_name="feeds-entry-detail", parents_lookup=['feed', ])
    _wordcounts = HyperlinkNestedViewField(view_name='feeds-entries-wordcount-list', parents_lookup=['entry__feed', 'entry', ], nested_field="wordcounts")
    
    class Meta:
        model = Entry
        fields = ('_url', '_wordcounts', 'feed', 'title', 'url', 'timestamp', 'text', )


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    #entries = EntryListSerializer(many=True, read_only=True)
    _entries = HyperlinkNestedViewField(view_name='feeds-entry-list', parents_lookup=['feed', ], nested_field="entries")
    
    class Meta:
        model = Feed
        fields = ('_url', '_entries', 'url', 'is_active', )
        read_only_fields = ('url', )

