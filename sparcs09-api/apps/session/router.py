from rest_framework import routers

from apps.session.viewsets import SessionViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(
    prefix=r'sessions',
    viewset=SessionViewSet,
    base_name='sessions',
)
router.register(
    prefix=r'users',
    viewset=UserViewSet,
    base_name='users',
)
