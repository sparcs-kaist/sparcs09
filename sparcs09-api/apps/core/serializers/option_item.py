from rest_framework import serializers

from apps.core.models import OptionItem


class OptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionItem
        fields = ['id', 'name', 'price_delta']
        read_only_fields = fields
