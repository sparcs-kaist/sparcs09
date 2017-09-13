from rest_framework import serializers

from apps.core.models import UserLog


class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = ['level', 'time', 'ip', 'group', 'text']
        read_only_fields = fields
