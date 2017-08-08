from django.contrib import admin

from apps.core.models import Comment, Content, Item, OptionCategory, \
    OptionItem, Payment, Record


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'price', 'join_type', 'created_date',
                    'deadline', 'delivery_date')
    list_filter = ('is_deleted', )


class ContentAdmin(admin.ModelAdmin):
    list_display = ('item', 'order', 'kind', 'content', 'image', 'link')
    list_filter = ('is_hidden', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('item', 'writer', 'content', 'created_date')
    list_filter = ('is_deleted', )


class OptionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'item')


class OptionItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price_delta')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('item', 'participant', 'total', 'status')


admin.site.register(Item, ItemAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(OptionCategory, OptionCategoryAdmin)
admin.site.register(OptionItem, OptionItemAdmin)
admin.site.register(Record)
admin.site.register(Payment, PaymentAdmin)
