from rest_framework.routers import DefaultRouter
from .views import CarViewSet, CustomerViewSet, RentalViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"cars", CarViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"rentals", RentalViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
