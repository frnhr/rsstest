import re
import string
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.html import strip_tags
import feedparser
import time
from api.models import Feed, Entry, Word


def tick(desc=None):
    if desc != False:
        if settings.DEBUG:
            print "{}tick: {}".format(
                "%s " % desc if desc else '',
                time.time() - tick.last
            )
    tick.last = time.time()


tick.last = 0


class Command(BaseCommand):
    help = 'Process all active feeds and count words'

    def handle(self, *args, **options):
        tick(False)
        for feed in Feed.objects.filter(is_active=True):
            tick(False)
            rss = feedparser.parse(feed.url)
            tick('Parse')
            for rss_entry in rss.entries:
                entry, just_created = Entry.objects.get_or_create(url=rss_entry.link, feed=feed)
                if just_created:
                    print u"processing {}".format(rss_entry.link)
                    entry.timestamp = timezone.now()
                    entry.title = rss_entry.title
                    entry.text = strip_tags(rss_entry.description)
                    entry.save()
                #@TODO handle situations when entry description changes

                if just_created:
                    wordcount = {}
                    tick(False)
                    words = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', entry.text.lower()).split()
                    tick('words list')
                    words.sort()
                    tick('words sort')
                    for word in words:
                        if word not in wordcount:
                            wordcount[word] = 1
                        else:
                            wordcount[word] += 1
                    tick('words count')
                    for word, count in wordcount.iteritems():
                        word = Word.objects.get_or_create(entry=entry, word=word)[0]  # (word, created)[0]
                        word.count += count
                        word.save()
                    tick('words save')
        print u"done"