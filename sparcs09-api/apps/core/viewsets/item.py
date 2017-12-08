import logging

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from apps.core.models import Content, Item, Payment, UserLog
from apps.core.permissions import IsItemHostOrReadOnly
from apps.core.serializers import (
    CommentCreateSerializer, CommentFullSerializer, CommentSerializer,
    ContentCreateSerializer, ContentSerializer,
    ItemCreateSerializer, ItemSerializer, ItemUpdateSerializer,
    PaymentCreateSerializer, PaymentSerializer,
)
from apps.core.utils import get_limit_offset, to_int


logger = logging.getLogger(UserLog.GROUP_ITEM)
logger_item = logging.getLogger(UserLog.GROUP_ITEM)
logger_comment = logging.getLogger(UserLog.GROUP_COMMENT)
logger_payment = logging.getLogger(UserLog.GROUP_PAYMENT)


class ItemViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '\d+'
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsItemHostOrReadOnly]

    def get_queryset_for_list(self):
        limit, offset = get_limit_offset(self.request.query_params)
        status = to_int(self.request.query_params.get('status', ''), 0)
        if status == 0:
            return Item.objects.filter(is_deleted=False)[offset:offset+limit]

        sid = self.request.query_params.get('sid', '')

        if status > 128 or status < 0:
            raise ParseError('Wrong status number')

        # status except 2 requires sid
        if status & 0b111101 != 0 and sid == '':
            raise ParseError('sid is required')

        queryset = Item.objects.none()

        # 1 - Not joined and Opened
        if status & 1:
            item_ids = (Payment.objects.filter(participant__username=sid)
                        .values_list('item', flat=True)
                        )
            query_1 = Item.objects.exclude(id__in=item_ids).filter(join_type=0)
            queryset |= query_1

        # 2 - Closed
        if status & 2:
            query_2 = Item.objects.filter(join_type=1)
            queryset |= query_2

        # 4 - Banned
        # 8 - Pending
        # 16 - Joined
        # 32 - Disputed
        # 64 - Paid
        # 128 - Confirmed
        for i in range(6):
            if status & (2 ** (i+2)):
                item_ids = (Payment.objects.filter(participant__username=sid,
                                                   status=i)
                            .values_list('item', flat=True)
                            )
                query_item = Item.objects.filter(id__in=item_ids)
                queryset |= query_item

        print(queryset)
        queryset = queryset.filter(is_deleted=False)
        print(queryset)

        return queryset[offset:offset+limit]

    # [GET] /items/
    def list(self, request):
        queryset = self.get_queryset_for_list()
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # [POST] /items/
    def create(self, request):
        data = request.data
        serializer = ItemCreateSerializer(data=data, context={
            'host': request.user}
        )

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            item = serializer.save()

        serializer_read = ItemSerializer(item)

        logger_item.info('create', {
            'r': request,
            'extra': {
                **serializer_read.data,
            },
        })

        return Response(serializer_read.data, status=status.HTTP_201_CREATED)

    # [GET] /items/<pk>/
    def retrieve(self, request, pk=None):
        item = self.get_object()
        if item.is_deleted:
            return Response({
                'detail': 'This item is deleted'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item)
        return Response(serializer.data)

    # [PUT] /items/<pk>/
    def update(self, request, pk=None):
        return Response({
            'detail': 'Method update to item is not allowed.',
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # [PATCH] /items/<pk>/
    def partial_update(self, request, pk=None):
        item = self.get_object()
        serializer = ItemUpdateSerializer(item, data=request.data,
                                          partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            item = serializer.save()

        serializer_read = ItemSerializer(item)

        logger_item.info('update', {
            'r': request,
            'extra': {
                **serializer_read.data,
            },
        })

        return Response(serializer_read.data, status=status.HTTP_200_OK)

    # [DELETE] /items/<pk>/
    def destroy(self, request, pk=None):
        item = self.get_object()

        if Payment.objects.filter(id=item.id).exists():
            return Response({
                'detail': 'Item cannot be deleted if payment exists.',
            }, status=status.HTTP_400_BAD_REQUEST)

        if item.is_deleted:
            return Response({
                'detail': 'This item is alreay deleted.',
            }, status=status.HTTP_400_BAD_REQUEST)

        item.is_deleted = True
        item.save()

        logger_item.info('delete', {
            'r': request,
            'extra': {
                'item': pk
            },
        })
        return Response(status=status.HTTP_200_OK)

    # [PATCH] /items/<pk>/
    @detail_route(methods=['patch'])
    def close(self, request, pk=None):
        item = self.get_object()
        item.deadline = timezone.now()
        item.save()

        logger_item.info('close', {
            'r': request,
            'extra': {
                'item': pk
            },
        })

        return Response(status=status.HTTP_200_OK)

    # [GET, POST] /items/<pk>/contents/
    @detail_route(methods=['get', 'post'])
    def contents(self, request, pk=None):
        item = self.get_object()
        return {
            'GET': self.contents_get,
            'POST': self.contents_post,
        }[request.method](request, item)

    def contents_get(self, request, item):
        payload = {
            'contents': [],
        }
        contents = Content.objects.filter(item=item).order_by('order')
        payload['contents'] = [ContentSerializer(c).data for c in contents]
        return Response(payload)

    def contents_post(self, request, item):
        serializer = ContentCreateSerializer(data=request.data, context={
          'item': item,
        })
        if not serializer.is_valid():
            return Response({
                'detail': 'Not valid data',
                'errors': serializer.errors,
            }, status=400)
        content = serializer.save()

        serializer_read = ContentSerializer(content)
        return Response({
            'content': serializer_read.data,
        })

    # [GET, POST] /items/<pk>/payments/
    @detail_route(methods=['get', 'post'])
    def payments(self, request, pk=None):
        item = self.get_object()
        return {
            'GET': self.payments_get,
            'POST': self.payments_post,
        }[request.method](request, item)

    # [GET] /items/<pk>/payments/
    def payments_get(self, request, item):
        limit, offset = get_limit_offset(request.GET)

        payload = {
            'total': 0,
            'payment_me': {},
            'payment_others': [],
        }

        payments = Payment.objects.filter(item=item)
        payload['total'] = payments.count()

        if request.user.is_authenticated:
            payment_me = payments.filter(participant=request.user).first()
            if payment_me:
                payload['payment_me'] = PaymentSerializer(payment_me).data

        if item.host == request.user:
            payment_others = payments[limit:limit+offset].all()
            for payment_other in payment_others:
                payload['payment_others'].append(
                    PaymentSerializer(payment_other).data
                )
        return Response(payload)

    # [POST] /items/<pk>/payments/
    def payments_post(self, request, item):
        serializer = PaymentCreateSerializer(data=request.data, context={
            'item': item,
            'participant': request.user,
        })
        if not serializer.is_valid():
            return Response({
                'detail': 'Not valid data.',
                'errors': serializer.errors,
            }, status=400)

        payment = serializer.save()

        logger_payment.info('create', {
            'r': request,
            'extra': {
                'item': item.id,
                'payment': payment.id,
                **serializer.validated_data,
            },
        })
        serializer_read = PaymentSerializer(payment)
        return Response({
            'payment': serializer_read.data,
        })

    # [GET, POST] /items/<pk>/comments/
    @detail_route(methods=['get', 'post'])
    def comments(self, request, pk=None):
        item = self.get_object()
        return {
            'GET': self.comments_get,
            'POST': self.comments_post,
        }[request.method](request, item)

    # [GET] /items/<pk>/comments/
    def comments_get(self, request, item):
        limit, offset = get_limit_offset(request.GET)
        sort_opt = request.GET.get('sort', 'id')

        response = []
        comments = item.comments.order_by(sort_opt)[offset:offset+limit]
        for comment in comments:
            serializer_class = CommentSerializer
            if request.user in [comment.writer, item.host]:
                serializer_class = CommentFullSerializer
            response.append(serializer_class(comment).data)

        return Response({
            'count': item.comments.all().count(),
            'comments': response,
        })

    # [POST] /items/<pk>/comments/
    def comments_post(self, request, item):
        serializer = CommentCreateSerializer(data=request.data, context={
            'item': item,
            'writer': request.user,
        })
        if not serializer.is_valid():
            return Response({
                'detail': 'Not valid data.',
                'errors': serializer.errors,
            }, status=400)

        serializer.save()

        logger_comment.info('write', {
            'r': request,
            'extra': {
                'item': item.id,
                **serializer.validated_data,
            },
        })
        return Response({
            'comment': serializer.data,
        })
