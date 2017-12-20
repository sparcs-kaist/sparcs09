from rest_framework import serializers
from rest_framework.serializers import ValidationError

from apps.core.models import Content


CONTENT_TYPE_TEXT = 0
CONTENT_TYPE_IMAGE = 1
CONTENT_TYPE_VIDEO = 2


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = [
            'id', 'order', 'kind',
            'content', 'image', 'link',
            'is_hidden',
        ]
        read_only_fields = fields


class ContentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = ['kind', 'content', 'image', 'link']

    def text_valid(self, data):
        return (
                not data['content'] is None and
                data['image'] is None and
                data['link'] is None
        )

    def image_valid(self, data):
        return (
                data['content'] is None and
                not data['image'] is None and
                data['link'] is None
        )

    def link_valid(self, data):
        return (
                data['content'] is None and
                data['image'] is None and
                not data['link'] is None
        )

    def validate(self, data):
        if not data['kind'] in [0, 1, 2]:
            raise ValidationError('Invalid type.')
        validators = [self.text_valid, self.image_valid, self.link_valid]
        if not validators[data['kind']](data):
            raise ValidationError('Content type mismatch.')
        return super().validate(data)

    def create(self, validated_data):
        item = self.context['item']

        content = Content(
            item=item,
            order=validated_data['order'],
            kind=validated_data['kind'],
            content=validated_data['content'],
            image=validated_data['image'],
            link=validated_data['link'],
        )
        content.save()

        return content


class ContentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = ['is_hidden']

    def validate(self, data):
        item = self.context['item']
        user = self.context['user']
        is_host = user == item.host

        if not is_host:
            raise ValidationError({
                'user': 'Editing contents is only available to host',
            })

        return data

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
