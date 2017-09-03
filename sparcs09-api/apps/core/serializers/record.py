from rest_framework import serializers
from rest_framework.serializers import ValidationError

from apps.core.models import OptionItem, Record


class RecordSerializer(serializers.ModelSerializer):
    option_ids = serializers.PrimaryKeyRelatedField(
        source='options', many=True, read_only=True,
    )

    class Meta:
        model = Record
        fields = ['option_ids', 'quantity']
        read_only_fields = fields


class RecordCreateSerializer(serializers.ModelSerializer):
    option_ids = serializers.ListField(
        child=serializers.IntegerField(),
    )
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Record
        fields = ['option_ids', 'quantity']

    def validate_option_ids(self, value):
        error_msg = 'Your options are not matched with the items'

        category_selection = {}
        for option_id in value:
            option_item = OptionItem.objects.filter(id=option_id).first()
            if option_item is None:
                raise ValidationError(error_msg)

            category_id = option_item.category.id
            if category_id in category_selection:
                raise ValidationError(error_msg)
            category_selection[category_id] = option_item

        categories = self.context['item'].option_categories.all()
        for category in categories:
            if category.required and category.id not in category_selection:
                raise ValidationError(error_msg)
        return value
