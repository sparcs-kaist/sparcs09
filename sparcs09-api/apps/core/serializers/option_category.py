from rest_framework import serializers

from apps.core.models import OptionCategory
from .option_item import OptionItemCreateSerializer, OptionItemSerializer


class OptionCategorySerializer(serializers.ModelSerializer):
    items = OptionItemSerializer(source='option_items', many=True)

    class Meta:
        model = OptionCategory
        fields = ['id', 'name', 'items', 'required']
        read_only_fields = fields


class OptionCategoryCreateSerializer(serializers.ModelSerializer):
    option_items = OptionItemCreateSerializer(many=True)

    class Meta:
        model = OptionCategory
        fields = ['name', 'required', 'option_items']
