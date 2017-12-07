from rest_framework import serializers
from rest_framework.serializers import ValidationError

from apps.session.models import UserProfile


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    sid = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    name = serializers.CharField(source='user.first_name', max_length=150)

    class Meta:
        model = UserProfile
        fields = [
            'sid', 'email', 'name',
            'phone', 'address', 'kakao_id', 'terms_agreed'
        ]
        extra_kwargs = {
            'phone': {'allow_blank': True},
            'address': {'allow_blank': True},
            'kakao_id': {'allow_blank': True},
        }

    def validate(self, data):
        if not data.get('terms_agreed', self.instance.terms_agreed):
            raise ValidationError({
                'terms_agreed': 'You should agree to our terms',
            })
        return super().validate(data)

    def update(self, instance, validated_data):
        instance.user.first_name = validated_data.pop('user', {}).pop(
            'first_name', instance.user.first_name
        )
        instance.user.save()
        return super().update(instance, validated_data)
