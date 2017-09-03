from rest_framework import serializers

from apps.core.models import OptionCategory
from .option_item import OptionItemSerializer


class OptionCategorySerializer(serializers.ModelSerializer):
    items = OptionItemSerializer(source='option_items', many=True)

    class Meta:
        model = OptionCategory
        fields = ['id', 'name', 'items']
        read_only_fields = fields
