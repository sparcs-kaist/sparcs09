from rest_framework import serializers
from rest_framework.serializers import ValidationError


FIELDS_MAX_LEN = {
    'name': 150,
    'phone': 100,
    'address': 500,
    'kakao_id': 100,
}


class UserSerializer(serializers.BaseSerializer):
    def __init__(self, *args, **kwargs):
        """
        show_private: a function that determines whether display the
             user's private fields (email. phone, address, kakao_id)
             it should be one of the followings:
             1. None (regarded as False)
             2. a boolean value
        """
        self.show_private = kwargs.pop('show_private', None)
        super(UserSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        validated_data = {}

        terms_agreed = data.get(
            'terms_agreed', self.instance.profile.terms_agreed
        )
        if not isinstance(terms_agreed, bool) or not terms_agreed:
            raise ValidationError({
                'terms_agreed': 'You should agree the terms.',
            })
        validated_data['terms_agreed'] = terms_agreed

        for key, value in data.items():
            if key == 'terms_agreed':
                continue

            max_len = FIELDS_MAX_LEN.get(key, 0)
            if not isinstance(value, str):
                raise ValidationError({
                    key: 'This field should be string',
                })
            elif key == 'name' and not value.strip():
                raise ValidationError({
                    key: 'This field is required.',
                })
            elif value and len(value) > max_len:
                raise ValidationError({
                    key: f'May not be more than {max_len} characters.',
                })
            validated_data[key] = value
        return validated_data

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
