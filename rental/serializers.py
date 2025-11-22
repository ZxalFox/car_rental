from rest_framework import serializers
from .models import Car, Customer, Rental

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        password = attrs.get("password")
        if not self.instance and not password:
            raise serializers.ValidationError({"password": "Este campo é obrigatório."})
        if password == "":
            raise serializers.ValidationError({"password": "Não pode ser vazio."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        return Customer.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = Customer
        fields = (
            "id",
            "username",
            "password",
            "email",
            "full_name",
            "document",
            "phone",
            "birth_date",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

class RentalSerializer(serializers.ModelSerializer):
    car_detail = CarSerializer(source="car", read_only=True)

    class Meta:
        model = Rental
        fields = (
            "id",
            "car",
            "customer",
            "start_date",
            "end_date",
            "agreed_daily_rate",
            "total_price",
            "odometer_start",
            "odometer_end",
            "pickup_location",
            "return_location",
            "status",
            "notes",
            "created_at",
            "updated_at",
            "car_detail",
        )
        read_only_fields = (
            "id",
            "customer",
            "total_price",
            "created_at",
            "updated_at",
            "car_detail",
        )

    def validate(self, attrs):
        start = attrs.get("start_date") or getattr(self.instance, "start_date", None)
        end = attrs.get("end_date") or getattr(self.instance, "end_date", None)
        car = attrs.get("car") or getattr(self.instance, "car", None)
        if start and end and not (start < end):
            raise serializers.ValidationError("start_date deve ser anterior a end_date")
        if car and start and end:
            exclude_id = getattr(self.instance, "pk", None)
            if Rental.has_conflict(car=car, start=start, end=end, exclude_id=exclude_id):
                raise serializers.ValidationError("Carro indisponível para o período informado.")
        return attrs
