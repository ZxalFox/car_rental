from rest_framework.routers import DefaultRouter

from .views import CarViewSet, CustomerViewSet, RentalViewSet

router = DefaultRouter()
router.register(r"cars", CarViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"rentals", RentalViewSet)

urlpatterns = router.urls
