from django.db import models
from django.utils import timezone


class Feed(models.Model):
    url = models.URLField(null=False, blank=False)
    is_active = models.BooleanField(null=False, blank=True, default=True)

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ['id', ]


class Entry(models.Model):
    feed = models.ForeignKey(Feed, related_name='entries', null=False)
    timestamp = models.DateTimeField()
    title = models.CharField(max_length=1000, null=False, blank=True, default=u'')
    text = models.TextField(null=False, blank=True, default=u'')
    url = models.URLField(null=False, blank=False, default=u'')

    def __unicode__(self):
        if self.title:
            return self.title
        return "(untitled entry)"

    def save(self, *args, **kwargs):
        if self.timestamp is None:
            self.timestamp = timezone.now()
        super(Entry, self).save(*args, **kwargs)


class WordCount(models.Model):
    word = models.ForeignKey('Word')
    entry = models.ForeignKey('Entry')
    count = models.PositiveIntegerField(default=0)


class Word(models.Model):
    word = models.CharField(max_length=255, null=False, blank=False, db_index=True, unique=True)
    entry = models.ManyToManyField(Entry, through=WordCount)

    def __unicode__(self):
        return self.word

    class Meta:
        ordering = ['word', ]


#@TODO another model for feed-level word counting, basically a cache?

