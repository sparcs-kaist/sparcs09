from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.models import Item, OptionCategory, OptionItem, Payment
from apps.core.serializers.option_category import (
    OptionCategoryCreateSerializer, OptionCategorySerializer,
)
from apps.session.serializers import UserPublicSerializer


class ItemCreateSerializer(serializers.ModelSerializer):
    option_categories = OptionCategoryCreateSerializer(many=True)
    price = serializers.IntegerField(min_value=100)

    class Meta:
        model = Item
        fields = ['title', 'description', 'thumbnail', 'price',
                  'payment_method', 'join_type', 'deadline',
                  'delivery_date', 'option_categories']

    def create(self, validated_data):
        categories = validated_data.pop('option_categories')
        item = Item.objects.create(
            created_date=timezone.now(),
            host=self.context['host'],
            **validated_data
        )

        for category_data in categories:
            option_items = category_data.pop('option_items')
            category = OptionCategory.objects.create(item=item,
                                                     **category_data)
            category.save()
            for option_item_data in option_items:
                option_item = OptionItem.objects.create(category=category,
                                                        **option_item_data)
                option_item.save()

        return item

    def validate(self, data):
        deadline = data.get('deadline')

        if deadline < timezone.now():
            raise ValidationError({
                'deadline': 'Deadline should be later than now'
            })

        if not (data.get('description') or data.get('thumbnail')):
            raise ValidationError({
                'description': 'Fill least one of description or thumbnail'
            })

        return super().validate(data)


class ItemSerializer(serializers.ModelSerializer):
    host = UserPublicSerializer()
    option_categories = OptionCategorySerializer(many=True)

    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'thumbnail', 'host', 'price',
                  'payment_method', 'join_type', 'created_date', 'deadline',
                  'delivery_date', 'is_deleted', 'option_categories']
        read_only_fields = fields


class ItemUpdateSerializer(serializers.ModelSerializer):
    option_categories = OptionCategoryCreateSerializer(many=True)

    class Meta:
        model = Item
        fields = ['title', 'description', 'thumbnail', 'price',
                  'payment_method', 'join_type', 'deadline',
                  'delivery_date', 'option_categories']

    def update(self, instance, validated_data):
        categories = validated_data.pop('option_categories', None)
        # read_only_fields = ['host', 'created_date', 'is_deleted']
        write_free_fields = ['deadline', 'delivery_date']

        payment_occured = Payment.objects.filter(item=instance.id).exists()

        for key, value in validated_data.items():
            if (key not in write_free_fields) and payment_occured:
                raise ValidationError({
                    key: f'{key} cannot be changed when payment exists'
                })
            instance.key = value
        instance.save()

        if categories is not None:
            if payment_occured:
                raise ValidationError({
                    'option_categories': 'Option cannot be changed'
                    'when payment exists'
                })

            current_categories = OptionCategory.objects.filter(
                item=instance.id
                )

            for category in current_categories:
                category.delete()

            for category_data in categories:
                option_items = category_data.pop('option_items')
                category = OptionCategory.objects.create(item=instance,
                                                         **category_data)
                category.save()
                for option_item_data in option_items:
                    option_item = OptionItem.objects.create(category=category,
                                                            **option_item_data)
                    option_item.save()

        return instance
