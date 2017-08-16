from rest_framework import serializers

from apps.core.models import Comment
from apps.session.serializers import UserFullSerializer, UserPublicSerializer


class CommentSerializer(serializers.ModelSerializer):
    writer = UserPublicSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'writer', 'created_date', 'is_deleted']
        read_only_fields = fields

    def to_representation(self, obj):
        result = super().to_representation(obj)
        if obj.is_deleted:
            result['content'] = 'DELETED'
        return result


class CommentFullSerializer(CommentSerializer):
    writer = UserFullSerializer()


class CommentCreateSerializer(serializers.ModelSerializer):
    writer = UserFullSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'writer', 'created_date', 'is_deleted']
        read_only_fields = ['id', 'created_date', 'is_deleted']

    def create(self, validated_data):
        validated_data['item'] = self.context['item']
        validated_data['writer'] = self.context['writer']
        return super().create(validated_data)
