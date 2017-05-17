from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import localtime


class Item(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_hidden = models.BooleanField()

    def __str__(self):
        return self.title


class Option(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    item = models.ForeignKey(Item, related_name='options',
                             on_delete=models.CASCADE)

    def __str__(self):
        return u'%s (%s KRW)' % (self.title, self.price)


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    num = models.IntegerField()

    def cost(self):
        return self.option.price * self.num

    def __str__(self):
        return u'%s %s: %d units' % (self.option.item, self.option, self.num)


class Payment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()
    is_paid = models.BooleanField()

    def __str__(self):
        return u'%s: %d for %s' % (self.user, self.total, self.item)


class UserLog(models.Model):
    """
    denotes single log for an user or global event
    - user:  user object
    - level: level of log; python log level
    - time:  event time
    - ip:    event ip
    - group: log group
    - text:  detail log message
    - is_hidden:  hide log in user log page
    """
    GROUP_ACCOUNT = 'sparcs09.account'
    GROUPS = [
        (GROUP_ACCOUNT, GROUP_ACCOUNT),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='logs', blank=True, null=True)
    level = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField()
    group = models.CharField(max_length=100, choices=GROUPS)
    text = models.CharField(max_length=500)
    is_hidden = models.BooleanField(default=False)

    def pretty(self):
        username = self.user.username if self.user else 'undefined'
        time_str = localtime(self.time).isoformat()
        return (f'{username}/{time_str} ({self.level}, {self.ip}) '
                '{self.group}.{self.text}')

    def __str__(self):
        time_str = localtime(self.time).isoformat()
        return (f'{time_str}/{self.level} ({self.user}) '
                '{self.group}.{self.text}')
