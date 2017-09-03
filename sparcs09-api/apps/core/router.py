from rest_framework import routers

from apps.core.viewsets import CommentViewSet, ItemViewSet, PaymentViewSet

router = routers.SimpleRouter()
router.register(
    prefix=r'items',
    viewset=ItemViewSet,
    base_name='items',
)
router.register(
    prefix=r'payments',
    viewset=PaymentViewSet,
    base_name='payments',
)
router.register(
    prefix=r'comments',
    viewset=CommentViewSet,
    base_name='comments',
)
