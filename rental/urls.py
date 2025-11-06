from django.urls import include, path

from . import views

app_name = "rental"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("rentals/nova/", views.RentalCreateView.as_view(), name="rental_create"),
    path("api/", include("rental.api_urls")),
]
