from rest_framework import viewsets
from .models import Car, Customer, Rental
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
