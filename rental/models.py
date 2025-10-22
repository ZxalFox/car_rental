import uuid
from django.db import models
from django.core.validators import MinValueValidator

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Car(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plate = models.CharField("Placa", max_length=10, unique=True)
    brand = models.CharField("Marca", max_length=50)
    model = models.CharField("Modelo", max_length=60)
    year = models.PositiveIntegerField("Ano")
    color = models.CharField("Cor", max_length=30, blank=True)
    odometer = models.PositiveIntegerField("Quilometragem", default=0)
    daily_rate = models.DecimalField("Preço por dia", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField("Ativo para locação", default=True)

    class Meta:
        ordering = ["brand", "model", "year"]

    def __str__(self):
        return f"{self.plate} - {self.brand} {self.model}/{self.year}"

class Customer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField("Nome completo", max_length=120)
    email = models.EmailField(unique=True)
    document = models.CharField("Documento (CPF/ID)", max_length=20, unique=True)
    phone = models.CharField("Telefone", max_length=20, blank=True)
    birth_date = models.DateField("Data de nascimento", null=True, blank=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name

class RentalStatus(models.TextChoices):
    RESERVED = "reserved", "Reservada"
    ONGOING = "ongoing", "Em curso"
    FINISHED = "finished", "Finalizada"
    CANCELED = "canceled", "Cancelada"

class Rental(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="rentals")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="rentals")
    start_date = models.DateField()
    end_date = models.DateField()
    agreed_daily_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], blank=True, default=0)
    odometer_start = models.PositiveIntegerField(null=True, blank=True)
    odometer_end = models.PositiveIntegerField(null=True, blank=True)
    pickup_location = models.CharField(max_length=120, blank=True)
    return_location = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=10, choices=RentalStatus.choices, default=RentalStatus.RESERVED)
    notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_date__lt=models.F("end_date")), name="rental_start_before_end"),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.car.plate} - {self.customer.full_name} ({self.start_date} → {self.end_date})"

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date and self.agreed_daily_rate:
            days = (self.end_date - self.start_date).days
            if days > 0:
                self.total_price = self.agreed_daily_rate * days
        super().save(*args, **kwargs)
