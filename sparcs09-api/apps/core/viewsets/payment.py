import logging

from rest_framework import viewsets
from rest_framework.response import Response

from apps.core.models import Payment, UserLog
from apps.core.permissions import IsParticipantOrNone
from apps.core.serializers import (
    PaymentSerializer, PaymentUpdateSerializer,
)

logger = logging.getLogger(UserLog.GROUP_PAYMENT)
logger_item = logging.getLogger(UserLog.GROUP_ITEM)


class PaymentViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '\d+'
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsParticipantOrNone]

    # [GET] /payments/
    def list(self, request):
        return Response({
            'detail': 'Listing is not allowed here.',
        }, status=405)

    # [POST] /payments/
    def create(self, request):
        return Response({
            'detail': 'Creating is not allowed here.',
        }, status=405)

    # [GET] /payments/<pk>/
    def retrieve(self, request, pk=None):
        payment = self.get_object()
        serializer = PaymentSerializer(payment)
        return Response({
            'payment': serializer.data,
        })

    # [PUT] /payments/<pk>/
    def update(self, request, pk=None):
        return Response({
            'detail': 'Updating is not allowed.',
        }, status=405)

    # [PATCH] /payments/<pk>/
    def partial_update(self, request, pk=None):
        payment = self.get_object()

        serializer = PaymentUpdateSerializer(
            payment, data=request.data, partial=True,
            context={
                'item': payment.item,
                'user': request.user,
            },
        )
        if not serializer.is_valid():
            return Response({
                'detail': 'Not valid data.',
                'errors': serializer.errors,
            }, status=400)

        serializer.save()

        logger.info('update', {
            'r': request,
            'extra': {
                'payment': payment.id,
                **serializer.validated_data,
            },
        })
        serializer_read = PaymentSerializer(payment)
        return Response({
            'payment': serializer_read.data,
        })

    # [DELETE] /payments/<pk>/
    def destroy(self, request, pk=None):
        payment = self.get_object()
        if payment.status not in [Payment.PENDING, Payment.JOINED]:
            return Response({
                'detail': 'Payment should be PENDING or JOINED state',
            })

        payment.delete()

        logger.info('delete', {
            'r': request,
            'extra': {'payment': payment.id},
        })
        return Response({})
