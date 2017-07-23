from rest_framework import serializers
from rest_framework.serializers import ValidationError


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=100, allow_blank=True)
    address = serializers.CharField(max_length=500, allow_blank=True)
    kakao_id = serializers.CharField(max_length=100, allow_blank=True)
    terms_agreed = serializers.BooleanField()

    def __init__(self, *args, **kwargs):
        """
        show_private: a function that determines whether display the
             user's private fields (email. phone, address, kakao_id)
             it should be one of the followings:
             1. None (regarded as False)
             2. a boolean value
        """
        self.show_private = kwargs.pop('show_private', None)
        super().__init__(*args, **kwargs)

    def validate_name(self, value):
        if not value.strip():
            raise ValidationError('Name is required')
        return value

    def validate(self, data):
        terms_agreed = data.get(
            'terms_agreed', self.instance.profile.terms_agreed,
        )
        if not isinstance(terms_agreed, bool) or not terms_agreed:
            raise ValidationError({
                'terms_agreed': 'You should agree to our terms',
            })
        return super().validate(data)

    def to_representation(self, obj):
        public_info = {
            'sid': obj.username,
            'name': obj.last_name,
        }
        private_info = {
            'email': obj.email,
            'phone': obj.profile.phone,
            'address': obj.profile.address,
            'kakao_id': obj.profile.kakao_id,
            'terms_agreed': obj.profile.terms_agreed,
        }

        if not self.show_private:
            return public_info
        return {**public_info, **private_info}

    def update(self, instance, validated_data):
        instance.last_name = validated_data.get('name', instance.last_name)
        instance.save()

        profile = instance.profile
        for name in ['phone', 'address', 'kakao_id', 'terms_agreed']:
            setattr(profile, name, validated_data.get(
                name, getattr(profile, name),
            ))
        profile.save()
        return instance
