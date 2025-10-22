from django.contrib import admin
from .models import Car, Customer, Rental

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("plate", "brand", "model", "year", "daily_rate", "is_active")
    list_filter = ("brand", "year", "is_active")
    search_fields = ("plate", "brand", "model")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "document", "phone")
    search_fields = ("full_name", "email", "document")

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("car", "customer", "start_date", "end_date", "status", "total_price")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("car__plate", "customer__full_name")
    autocomplete_fields = ("car", "customer")
