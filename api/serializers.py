from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.reverse import reverse
from api.models import Feed, Entry, Word


class HyperlinkNestedSelf(Field):
    url = None
    view_name = None
    parents_lookup = None
    self_field = None
    
    def __init__(self, view_name, parents_lookup=None, self_field='pk', *args, **kwargs):
        super(HyperlinkNestedSelf, self).__init__(*args, **kwargs)
        self.view_name = view_name
        self.parents_lookup = parents_lookup
        self.self_field = self_field
        
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


# detail serializers


class WordSerializer(serializers.HyperlinkedModelSerializer):
    _url = HyperlinkNestedSelf(view_name="feeds-entries-word-detail", parents_lookup=['entry__feed', 'entry', ])
    
    class Meta:
        model = Word
        fields = ('_url', 'word', 'count', 'entry', )



class EntrySerializer(serializers.HyperlinkedModelSerializer):
    _url = HyperlinkNestedSelf(view_name="feeds-entry-detail", parents_lookup=['feed', ])
    words = HyperlinkNestedViewField(view_name='feeds-entries-word-list', parents_lookup=['entry__feed', 'entry', ], nested_field="words")
    
    class Meta:
        model = Entry
        fields = ('_url', 'feed', 'title', 'timestamp', 'text', 'words', )


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    entries = EntryListSerializer(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = ('_url', 'url', 'is_active', 'entries', )
