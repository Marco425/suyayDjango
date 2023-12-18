from rest_framework.routers import DefaultRouter
from orders.api.views import OrderApiViewSet

router_order = DefaultRouter()

router_order.register(
    prefix='orders', basename='orders', viewset=OrderApiViewSet
)