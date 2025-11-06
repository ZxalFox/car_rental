from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import viewsets

from .forms import RentalForm
from .models import Car, Customer, Rental, RentalStatus
from .serializers import CarSerializer, CustomerSerializer, RentalSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.select_related("car", "customer").all()
    serializer_class = RentalSerializer


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
