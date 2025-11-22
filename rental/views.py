from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .forms import RentalForm
from .models import Car, Customer, Rental, RentalStatus
from .serializers import CarSerializer, CustomerSerializer, RentalSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        action = getattr(self, "action", None)
        if action == "list":
            include_inactive = self.request.query_params.get("include_inactive")
            if include_inactive in {"1", "true", "True"}:
                return queryset
            return queryset.filter(is_active=True)
        return queryset

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CustomerSerializer

    @action(detail=False, methods=["get"], url_path="me", permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.select_related("car", "customer").all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RentalSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(customer=self.request.user)

    @action(detail=False, methods=["get"], url_path="my")
    def my(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(customer=self.request.user)


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "rental/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_rentals"] = (
            Rental.objects.select_related("car")
            .filter(customer=self.request.user)
            .order_by("-start_date")
        )
        context["available_cars"] = Car.objects.filter(is_active=True).order_by("brand", "model")
        context["rental_status"] = RentalStatus
        return context


class RentalCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Rental
    form_class = RentalForm
    template_name = "rental/rental_form.html"
    success_message = "Reserva criada com sucesso."
    success_url = reverse_lazy("rental:dashboard")

    def get_initial(self):
        initial = super().get_initial()
        car_id = self.request.GET.get("car")
        if car_id:
            try:
                car = Car.objects.get(pk=car_id, is_active=True)
                initial["car"] = car
                initial.setdefault("agreed_daily_rate", car.daily_rate)
            except Car.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        form.instance.customer = self.request.user
        form.instance.status = RentalStatus.RESERVED
        if not form.cleaned_data.get("agreed_daily_rate") and form.instance.car:
            form.instance.agreed_daily_rate = form.instance.car.daily_rate
        return super().form_valid(form)
