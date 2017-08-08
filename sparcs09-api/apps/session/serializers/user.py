from django.contrib.auth.models import User

from rest_framework import serializers


class UserPublicSerializer(serializers.ModelSerializer):
    sid = serializers.ReadOnlyField(source='username')
    name = serializers.ReadOnlyField(source='first_name')

    class Meta:
        model = User
        fields = ['sid', 'name']


class UserFullSerializer(serializers.ModelSerializer):
    sid = serializers.ReadOnlyField(source='username')
    name = serializers.ReadOnlyField(source='first_name')
    phone = serializers.ReadOnlyField(source='profile.phone')
    address = serializers.ReadOnlyField(source='profile.address')
    kakao_id = serializers.ReadOnlyField(source='profile.kakao_id')
    terms_agreed = serializers.ReadOnlyField(source='profile.terms_agreed')

    class Meta:
        model = User
        fields = [
            'sid', 'email', 'name',
            'phone', 'address', 'kakao_id', 'terms_agreed',
        ]
        read_only_fields = ['email']
