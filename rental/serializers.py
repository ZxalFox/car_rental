from rest_framework import serializers
from .models import Car, Customer, Rental

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = "__all__"

    def validate(self, attrs):
        start = attrs.get("start_date") or getattr(self.instance, "start_date", None)
        end = attrs.get("end_date") or getattr(self.instance, "end_date", None)
        if start and end and not (start < end):
            raise serializers.ValidationError("start_date deve ser anterior a end_date")
        return attrs
