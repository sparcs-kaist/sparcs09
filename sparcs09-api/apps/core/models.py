from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import localtime


class Item(models.Model):
    """
    Represents a single 09 item.

    Attributes:
        title: the title of this item
        host: the manager of this item
        price: the default price - can be changed by option items
        join_type: the join type - one of JOIN_TYPE_CHOICES
        created_date: the created date
        deadline: the deadline - user cannot join 09 after this deadline
        delivery_date: expected delivery date (can be null)
        is_deleted: the deleted flag
    """

    JOIN_TYPE_OPEN = 0
    JOIN_TYPE_CLOSED = 1
    JOIN_TYPE_CHOICES = (
        (JOIN_TYPE_OPEN, 'Open'),
        (JOIN_TYPE_CLOSED, 'Closed')
    )
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='images/thumbnail/',
                                  null=True, blank=True)
    host = models.ForeignKey(User, related_name='items')
    price = models.IntegerField()
    payment_method = models.CharField(max_length=100,
                                      null=True, blank=True)
    join_type = models.IntegerField(choices=JOIN_TYPE_CHOICES)
    created_date = models.DateTimeField()
    deadline = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Content(models.Model):
    """
    Represents a text, image or video content of a 09 item.

    Attributes:
        item: the item that this content belongs to
        order: the order of this content in the item (starts from 1)
        type: the type of this content - one of CONTENT_TYPE_CHOICES
        content: the text messages (available iff type=0)
        image: the image file (available iff type=1)
        link: the link of the Youtube video (available iff type=2)
        is_hidden: the hidden flag - if true, it will be folded in the item
                   page as default
    """

    CONTENT_TYPE_TEXT = 0
    CONTENT_TYPE_IMAGE = 1
    CONTENT_TYPE_VIDEO = 2
    CONTENT_TYPE_CHOICES = (
        (CONTENT_TYPE_TEXT, 'Text'),
        (CONTENT_TYPE_IMAGE, 'Image'),
        (CONTENT_TYPE_VIDEO, 'Video'),
    )
    item = models.ForeignKey('Item', related_name='contents',
                             on_delete=models.CASCADE)
    order = models.IntegerField()
    kind = models.IntegerField(choices=CONTENT_TYPE_CHOICES)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/content',
                              null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    is_hidden = models.BooleanField(default=False)


class Comment(models.Model):
    """
    Represents a single comment on a 09 item.

    Attributes:
        item: the item that this comment belongs to
        content: the text of this comment
        writer: the writer of this comment
        created_date: the created datetime
        is_deleted: the deleted flag
    """

    item = models.ForeignKey('Item', related_name='comments',
                             on_delete=models.CASCADE)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)


class OptionCategory(models.Model):
    """
    Represents a option category of a 09 item.

    Attributes:
        name: the name of the option category
        item: the item that this option category belongs to
        required: flag whether this category selection is required or not
    """
    name = models.CharField(max_length=100)
    item = models.ForeignKey('Item', related_name='option_categories',
                             on_delete=models.CASCADE)
    required = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class OptionItem(models.Model):
    """
    Represents an option item of an option category.

    Attributes:
        name: the name of the option item
        price_delta: price difference respected to the item price
        category: the option category that this option item belongs to
    """

    name = models.CharField(max_length=100)
    price_delta = models.IntegerField(default=0)
    category = models.ForeignKey('OptionCategory', related_name='option_items',
                                 on_delete=models.CASCADE)


class Record(models.Model):
    """
    Represents a participation record for a payment + an option.

    Attributes:
        payment: the payment that this record belongs to
        options: list of option item that the user was selected - they should
                 be selected exactly one in each option categories of the item
        quantity: the quantity for the fixed options
    """
    payment = models.ForeignKey('Payment', related_name='records',
                                on_delete=models.CASCADE)
    options = models.ManyToManyField(OptionItem)
    quantity = models.IntegerField()

    @property
    def cost(self):
        return (self.payment.item.price + sum(map(
            lambda x: x.price_delta, self.options.all(),
        ))) * self.quantity


class Payment(models.Model):
    """
    Represents a payment record for an user + a 09 item.

    Attributes:
        item: the item that the user has been particiapted
        participant: the participated user
        total: total amount to pay - summation of record.cost()
        status: payment status - one of STATUS_CHOICES
        info: additional message to the host
    """
    STATUS_BANNED = 0
    STATUS_PENDING = 1
    STATUS_JOINED = 2
    STATUS_DISPUTED = 3
    STATUS_PAID = 4
    STATUS_CONFIRMED = 5
    STATUS_CHOICES = (
        (STATUS_BANNED, 'Banned'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_JOINED, 'Joined'),
        (STATUS_DISPUTED, 'In Disputed'),
        (STATUS_PAID, 'Paid'),
        (STATUS_CONFIRMED, 'Confirmed'),
    )
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.participant}: {self.total} for {self.item}'


class UserLog(models.Model):
    """
    Represents a single log for an user or global event.

    Attributes:
        user: the event user (none in case of global event)
        level: the event level - uses python log level convention
        time: the time of this event
        ip: the event ip (0.0.0.0 in case of unknown)
        group: the event group - one of GROUP_CHOICES
        text: the message of this event
        is_hidden: the hidden flag - hide from users iff true
    """
    GROUP_ACCOUNT = 'sparcs09.account'
    GROUP_COMMENT = 'sparcs09.comment'
    GROUP_ITEM = 'sparcs09.item'
    GROUP_PAYMENT = 'sparcs09.payment'
    GROUP_CHOICES = [
        (GROUP_ACCOUNT, GROUP_ACCOUNT),
        (GROUP_COMMENT, GROUP_COMMENT),
        (GROUP_ITEM, GROUP_ITEM),
        (GROUP_PAYMENT, GROUP_PAYMENT),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_logs', blank=True, null=True)
    level = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField()
    group = models.CharField(max_length=100, choices=GROUP_CHOICES)
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
