from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.html import strip_tags
import feedparser
from api.models import Feed, Entry


class Command(BaseCommand):
    help = 'Process all active feeds and count words'

    def handle(self, *args, **options):
        for feed in Feed.objects.filter(is_active=True):
            rss = feedparser.parse(feed.url)
            for rss_entry in rss.entries:
                entry, just_created = Entry.objects.get_or_create(url=rss_entry.link, feed=feed)
                if just_created:
                    entry.timestamp = timezone.now()
                    entry.title = rss_entry.title
                    entry.text = strip_tags(rss_entry.description)
                    entry.save()
                #@TODO handle situations when entry description changes
                
                if just_created:
                    pass
                    #@TODO count words

