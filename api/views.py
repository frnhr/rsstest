from json.decoder import JSONDecoder
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import is_client_error
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin
from api.models import Feed, Entry, WordCount
from .serializers import FeedListSerializer, EntryListSerializer, EntrySerializer, WordCountSerializer, FeedSerializer, \
    WordCountListSerializer, WordCountRootSerializer, WordCountTopSerializer


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


# noinspection PyUnresolvedReferences
class AggregateCountMixin(object):
    """
    Calculates a sun of all "count" fields.
    Not using SQL aggregation here, no need, and this way we can support ValuesQuerySet too.
    """
    def list(self, request, *args, **kwargs):
        response = super(AggregateCountMixin, self).list(request, *args, **kwargs)
        queryset = self.get_queryset()
        try:
            queryset.all()[0]['count']
        except TypeError:
            get_count = lambda item: item.count
        else:
            get_count = lambda item: item['count']
        count_sum = sum(get_count(item) for item in queryset.all())
        response.data.insert(3, 'count__sum', count_sum)
        return response


# noinspection PyUnresolvedReferences
class DatatableSupportMixin(object):

    def list(self, request, *args, **kwargs):
        if request.GET.get('draw', False):
            self.kwargs[self.page_kwarg] = int(request.GET['start']) / int(request.GET['length']) + 1
        response = super(DatatableSupportMixin, self).list(request, *args, **kwargs)
        if request.GET.get('draw', False):
            response.data['draw'] = int(request.GET['draw'])
            response.data['recordsTotal'] = response.data['results_count']
            response.data['recordsFiltered'] = response.data['results_count']
            response.data['data'] = response.data['results']
            del response.data['results']
        return response


class FeedViewSet(RenameResultsCountMixin, DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows feeds to be viewed, added, deleted and en/disabled.
    """
    queryset = Feed.objects.all()
    serializer_class = FeedListSerializer
    serializer_detail_class = FeedSerializer
    http_method_names = ('get', 'head', 'options', 'post', 'patch', 'delete', )


class EntryViewSet(RenameResultsCountMixin, DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows feed entries to be viewed.
    """
    http_method_names = ('get', 'head', 'options', )
    queryset = Entry.objects.all()
    serializer_class = EntryListSerializer
    serializer_detail_class = EntrySerializer


class WordCountViewSet(RenameResultsCountMixin, DetailSerializerMixin, NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows word counts in an entry to be viewed.
    """
    http_method_names = ('get', 'head', 'options', )
    queryset = WordCount.objects.all().order_by('-count')
    serializer_class = WordCountListSerializer
    serializer_detail_class = WordCountSerializer


# noinspection PyUnresolvedReferences
class QueryFilterMixin(object):
    def get_queryset(self, is_for_detail=False):
        queryset = super(QueryFilterMixin, self).get_queryset(is_for_detail)
        if not is_for_detail:
            queryset = self.filter_queryset(queryset)
        return queryset

    def filter_queryset(self, queryset):
        w, e, f = map(self.get_query().get, ('w', 'e', 'f'))
        if f and e:
            #@TODO this self.stuff thing is not the prettiest way of accomplishing this.
            # perhaps move this check to list()?
            # it tests thread-safe though.
            self.status = status.HTTP_406_NOT_ACCEPTABLE
            self.message = u'Please use either "f" or "e" query, not both.'

        if w:  # word
            queryset = queryset.filter(word__word=w.lower())

        if e:  # entry
            try:
                e_int = int(e)
            except ValueError:
                e_int = False
            if e_int and str(e_int) == e:  # ?e=<id>
                queryset = queryset.filter(entry__id=e_int).distinct()
            else:  # ?e=<url>
                queryset = queryset.filter(entry__url=e).distinct()

        if f:  # feed
            try:
                f_int = int(f)
            except ValueError:
                f_int = False
            if f_int and str(f_int) == f:  # ?f=<id>
                queryset = queryset.filter(entry__feed__id=f_int).distinct()
            else:  # ?f=<url>
                queryset = queryset.filter(entry__feed__url=f).distinct()

        return queryset.order_by('-count')

    def get_query(self):
        w = self.request.GET.get('w', None)
        f = self.request.GET.get('f', None)  # url decoded behind-the-scene
        e = self.request.GET.get('e', None)  # url decoded behind-the-scene
        return {
            'w': w,
            'e': e,
            'f': f,
        }


class WordCountRootViewSet(AggregateCountMixin, QueryFilterMixin, RenameResultsCountMixin, DetailSerializerMixin, viewsets.ModelViewSet):
    """
    API endpoint that shows word counts per entries. Allows querying for word, entry and feed.

    Usage: ?f=http://blog.codinghorror.com/rss/
      - lists all words in all entries of that feed
      - words will appear multiple times, once for each entry!

    Usage: ?e=http://blog.codinghorror.com/the-just-in-time-theory/
      - lists all words one selected entry
      - words are distinct

    Usage: ?w=the
      - lists all entries where word "the" appears
      - words will appear multiple times, once for each entry!

    Usage: ?w=the&feed=1
      - lists all entries in a feed where word "the" appears
      - feeds (and entries) can be identified using wither their external URL or internal ID
      - words will appear multiple times, once for each entry!

    Response:
    {
        "results_count": 23,   //////// number of words found in current query
        "next": "http://localhost:8000/words/?feed=1&page=2&w=the", //////// pagination 
        "previous": null,  //////// pagination
        "count__sum": 817,  //////// sum of all word counts in current query 
        "results": [
            {   //////// details about one word-entry pair
                "_url": "http://localhost:8000/feeds/1/entries/8/wordcounts/1966/", 
                "word": "the", 
                "count": 94, 
                "entry": "http://localhost:8000/feeds/1/entries/8/", 
                "entry_title": "App-pocalypse Now", 
                "feed_url": "http://blog.codinghorror.com/rss/"
            },
            ...
        ]
    }
    """
    http_method_names = ('get', 'head', 'options', )
    queryset = WordCount.objects.all()
    serializer_class = WordCountRootSerializer
    serializer_detail_class = WordCountRootSerializer

    status = 200
    message = ''

    def list(self, request, *args, **kwargs):
        """
        Add a few additional fields to this ListView
        """
        response = super(WordCountRootViewSet, self).list(request, *args, **kwargs)
        if is_client_error(self.status):
            return Response(self.message, status=self.status)
        query_dict = self.request.GET.copy()
        if 'page' in query_dict.keys():
            del query_dict['page']
        response.data.insert(4, '_simple', reverse('wordcounts-simple-list', request=self.request) + ("?{}".format(query_dict.urlencode()) if query_dict else ''))
        response.data.insert(5, '_simple_json', reverse('wordcounts-json-list', request=self.request))
        return response


class WordCountSimpleViewSet(WordCountRootViewSet):
    """
    Simplified API endpoint, same as /wordcounts, but with only count__sum as output. 
    """
    serializer_class = WordCountRootSerializer

    def list(self, request, *args, **kwargs):
        response = super(WordCountSimpleViewSet, self).list(request, *args, **kwargs)
        if response.status_code != status.HTTP_200_OK:
            return response
        return Response(response.data.get('count__sum', 0), status.HTTP_200_OK)


class WordCountSimpleJsonViewSet(WordCountSimpleViewSet):
    """
    Simplified API endpoint, same as /wordcounts/simple, but it takes JSON query and responds to POST (instead of query parameters and GET).
    Sample JSON query object:
    {
    "w": "the",
    "f": "http://blog.codinghorror.com/rss/"
    }
    Note: JSON does not support single quotes!!!11
    Note2: Don't forget content-type: application/json 
    """

    json_query = None
    empty_query = {
        'w': None,
        'e': None,
        'f': None,
    }

    def http_method_not_allowed(self, request, *args, **kwargs):
        """
        If `request.method` does not correspond to a handler method,
        determine what kind of exception to raise.
        """
        if request.method == 'POST':
            # noinspection PyUnresolvedReferences
            return self.get(request, *args, **kwargs)
        super(WordCountSimpleJsonViewSet, self).http_method_not_allowed(request, *args, **kwargs)

    def get_query(self):
        """
        Fetch query valued from request body instead from URL query parameters.
        """
        if self.request.method == 'POST':
            if self.json_query is None:
                body = self.request.body.strip()
                if not body:
                    body = '{}'  # allow empty POST
                try:
                    self.json_query = JSONDecoder().decode(body)
                except ValueError as e:
                    self.status = status.HTTP_406_NOT_ACCEPTABLE
                    self.message = "JSON decode error: {}".format(e.message)
        return self.empty_query if not self.json_query else self.json_query


class WordCountTopViewSet(DatatableSupportMixin, QueryFilterMixin, AggregateCountMixin, RenameResultsCountMixin,
                          ListModelMixin, GenericAPIView, viewsets.ViewSet):
    serializer_class = WordCountTopSerializer

    def get_queryset(self, is_for_detail=False):
        #@TODO add query support
        queryset = WordCount.objects.all()
        queryset = self.filter_queryset(queryset)
        queryset = queryset.values('word__word').annotate(count=Sum('count')).order_by("-count", "word__word")
        return queryset
