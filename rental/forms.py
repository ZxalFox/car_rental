from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Car, Rental, RentalStatus


class RentalForm(forms.ModelForm):
    start_date = forms.DateField(
        label=_("Data de início"),
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = forms.DateField(
        label=_("Data de término"),
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    agreed_daily_rate = forms.DecimalField(
        label=_("Valor por dia"),
        min_value=0,
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={"step": "0.01"}),
    )

    class Meta:
        model = Rental
        fields = (
            "car",
            "start_date",
            "end_date",
            "agreed_daily_rate",
            "pickup_location",
            "return_location",
            "notes",
        )
        widgets = {
            "pickup_location": forms.TextInput(attrs={"placeholder": "Local de retirada"}),
            "return_location": forms.TextInput(attrs={"placeholder": "Local de devolução"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["car"].queryset = Car.objects.filter(is_active=True)
        self.fields["car"].label = _("Carro")
        self.fields["pickup_location"].label = _("Retirada")
        self.fields["return_location"].label = _("Devolução")
        self.fields["notes"].label = _("Notas")

    def clean(self):
        cleaned_data = super().clean()
        car = cleaned_data.get("car")
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        if not car or not start or not end:
            return cleaned_data
        exclude = self.instance.pk if getattr(self.instance, "pk", None) else None
        if Rental.has_conflict(car=car, start=start, end=end, exclude_id=exclude):
            raise forms.ValidationError(
                _("Este carro já está reservado para o período selecionado."),
            )
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            if not instance.pk:
                instance.status = RentalStatus.RESERVED
            instance.save()
            self.save_m2m()
        return instance
