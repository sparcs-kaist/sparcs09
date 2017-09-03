from rest_framework import serializers
from rest_framework.serializers import ValidationError

from apps.core.models import Item, OptionItem, Payment, Record
from apps.session.serializers import UserFullSerializer
from .record import RecordCreateSerializer, RecordSerializer


# state (from -> to): permission (host, participant)
STATUS_TRANSITIONS = {
    (Payment.STATUS_BANNED, Payment.STATUS_JOINED): (True, False),
    (Payment.STATUS_PENDING, Payment.STATUS_BANNED): (True, False),
    (Payment.STATUS_PENDING, Payment.STATUS_JOINED): (True, False),
    (Payment.STATUS_JOINED, Payment.STATUS_BANNED): (True, False),
    (Payment.STATUS_JOINED, Payment.STATUS_PAID): (False, True),
    (Payment.STATUS_DISPUTED, Payment.STATUS_PAID): (False, True),
    (Payment.STATUS_DISPUTED, Payment.STATUS_JOINED): (False, True),
    (Payment.STATUS_DISPUTED, Payment.STATUS_CONFIRMED): (True, False),
    (Payment.STATUS_PAID, Payment.STATUS_JOINED): (False, True),
    (Payment.STATUS_PAID, Payment.STATUS_DISPUTED): (True, False),
    (Payment.STATUS_PAID, Payment.STATUS_CONFIRMED): (True, False),
}


def save_records(payment, records):
    total = 0
    for record_data in records:
        option_items = list(map(
            lambda x: OptionItem.objects.get(id=x),
            record_data['option_ids'],
        ))
        record = Record(
            payment=payment,
            quantity=record_data['quantity'],
        )
        record.save()
        record.options.add(*option_items)
        record.save()
        total += record.cost

    payment.total = total
    payment.save()


class PaymentSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(source='item', read_only=True)
    participant = UserFullSerializer()
    records = RecordSerializer(many=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'item_id', 'participant', 'status',
            'total', 'info', 'records'
        ]
        read_only_fields = fields


class PaymentCreateSerializer(serializers.ModelSerializer):
    records = RecordCreateSerializer(many=True)

    class Meta:
        model = Payment
        fields = ['records']

    def validate(self, data):
        payment_count = Payment.objects.filter(
            item=self.context['item'],
            participant=self.context['participant'],
        ).count()
        if payment_count > 0:
            raise ValidationError('Already registered.')
        return super().validate(data)

    def create(self, validated_data):
        item = self.context['item']
        participant = self.context['participant']

        status = Payment.STATUS_PENDING
        if item.join_type == Item.JOIN_TYPE_OPEN:
            status = Payment.STATUS_JOINED

        payment = Payment(
            item=item,
            participant=participant,
            total=0,
            status=status,
        )
        payment.save()

        save_records(payment, validated_data['records'])
        return payment


class PaymentUpdateSerializer(serializers.ModelSerializer):
    records = RecordCreateSerializer(many=True)

    class Meta:
        model = Payment
        fields = ['records', 'status', 'info']

    def validate(self, data):
        payment, user = self.instance, self.context['user']
        is_host = user == payment.item.host
        is_participant = user == payment.participant

        has_record = len(data.pop('records', [])) > 0
        has_status = 'status' in data and (payment.status != data['status'])
        has_info = 'info' in data

        if has_record:
            if not is_participant:
                raise ValidationError({
                    'user': 'Editing records is only available to participant',
                })
            elif has_status:
                raise ValidationError({
                    'status': 'Status should be null when changing records',
                })
            elif payment.status != Payment.STATUS_JOINED:
                raise ValidationError({
                    'status': 'Current status should be JOINED',
                })

        if has_status:
            if has_record:
                raise ValidationError({
                    'records': 'Records should be null when changing status',
                })

            perm = STATUS_TRANSITIONS.get(
                (payment.status, data['status']), (False, False)
            )
            perm_host = perm[0] and is_host
            perm_participant = perm[1] and is_participant
            if not perm_host and not perm_participant:
                raise ValidationError({
                    'status': 'Requested transition is not allowed',
                })

        if has_info:
            if not is_participant:
                raise ValidationError({
                    'info': 'Editing info is only available to participant',
                })

        return data

    def update(self, instance, validated_data):
        records = validated_data.pop('records', [])
        if records:
            instance.records.all().delete()
            save_records(instance, records)
        return super().update(instance, validated_data)
