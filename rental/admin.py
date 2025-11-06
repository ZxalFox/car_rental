from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Car, Customer, Rental

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("plate", "brand", "model", "year", "daily_rate", "is_active")
    list_filter = ("brand", "year", "is_active")
    search_fields = ("plate", "brand", "model")

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Informações adicionais",
            {
                "fields": (
                    "full_name",
                    "document",
                    "phone",
                    "birth_date",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informações adicionais",
            {
                "classes": ("wide",),
                "fields": (
                    "full_name",
                    "document",
                    "phone",
                    "birth_date",
                ),
            },
        ),
    )
    list_display = ("username", "full_name", "email", "document", "is_active")
    search_fields = ("username", "full_name", "email", "document")
    readonly_fields = ("created_at", "updated_at")

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("car", "customer", "start_date", "end_date", "status", "total_price")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("car__plate", "customer__full_name")
    autocomplete_fields = ("car", "customer")
