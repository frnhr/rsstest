import sys
import inspect
from django.contrib import admin
from api.models import Feed, Entry, Word, WordCount


class FeedAdmin(admin.ModelAdmin):
    model = Feed
    list_display = ('__unicode__', 'is_active',)
    list_filter = ('is_active',)
    
    
class EntryAdmin(admin.ModelAdmin):
    model = Entry
    list_display = ('__unicode__', 'feed', )
    list_filter = ('feed',)
    
    
class WordCountInline(admin.TabularInline):
    model = WordCount
    extra = 0
    
    
class WordAdmin(admin.ModelAdmin):
    model = Word
    list_filter = ['entry__feed', 'entry', ]
    search_fields = ('word', )
    inlines = (WordCountInline, )
    

# auto-register ModelAdmin classes:

classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for name, cls in classes:
    if issubclass(cls, admin.ModelAdmin) and hasattr(cls, 'model') and 'Mixin' not in name and not issubclass(cls, admin.options.InlineModelAdmin):
        admin.site.register(cls.model, cls)
        