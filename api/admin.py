import sys
import inspect
from django.contrib import admin
from api.models import Feed, Entry, Word


class FeedAdmin(admin.ModelAdmin):
    model = Feed
    
    
class EntryAdmin(admin.ModelAdmin):
    model = Entry
    
    
class WordAdmin(admin.ModelAdmin):
    model = Word
    list_filter = ['entry__feed', ]
    

# auto-register ModelAdmin classes:

classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for name, cls in classes:
    if issubclass(cls, admin.ModelAdmin) and hasattr(cls, 'model') and 'Mixin' not in name and not issubclass(cls, admin.options.InlineModelAdmin):
        admin.site.register(cls.model, cls)
        