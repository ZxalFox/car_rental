from django.urls import path
from rest_framework.routers import DefaultRouter

from .api_views import SessionLoginView, SessionLogoutView, SessionView
from .views import CarViewSet, CustomerViewSet, RentalViewSet

router = DefaultRouter()
router.register(r"cars", CarViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"rentals", RentalViewSet)

urlpatterns = router.urls + [
	path("session/", SessionView.as_view(), name="api-session"),
	path("session/login/", SessionLoginView.as_view(), name="api-session-login"),
	path("session/logout/", SessionLogoutView.as_view(), name="api-session-logout"),
]
