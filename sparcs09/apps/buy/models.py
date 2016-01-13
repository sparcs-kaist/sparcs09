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
        return u'%s (%s KRW)' % (self.title, self.price)


class Record(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(Option)
    num = models.IntegerField()

    def cost(self):
        return self.option.price * self.num

    def __unicode__(self):
        return u'%s %s: %d units' % (self.option.item, self.option, self.num)


class Payment(models.Model):
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
    total = models.IntegerField()
    is_paid = models.BooleanField()

    def __unicode__(self):
        return u'%s: %d for %s' % (self.user, self.total, self.item)
