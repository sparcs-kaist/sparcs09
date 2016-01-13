from django.contrib import admin
from sparcs09.apps.buy.models import Item, Option, Record


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'valid_from', 'valid_to', 'is_hidden')
    list_filter = ('is_hidden', )


class OptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'item')


class RecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'num')


admin.site.register(Item, ItemAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Record, RecordAdmin)
