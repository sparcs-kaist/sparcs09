from django.contrib.auth.models import User
from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_hidden = models.BooleanField()

    def __unicode__(self):
        return self.title


class Option(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    item = models.ForeignKey(Item, related_name='options')

    def __unicode__(self):
        return u'%s %s (%s KRW)' % (self.item, self.title, self.price)


class Record(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(Option)
    num = models.IntegerField()

    def __unicode__(self):
        return u'%s: %d units' % (self.option, self.num)
