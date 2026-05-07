# newApp/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Profile, MaintenanceRecord
from datetime import datetime


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class ProfileUpdateForm(forms.ModelForm):
    car_year = forms.TypedChoiceField(
        choices=[],
        coerce=int,
        required=False,
    )

    class Meta:
        model = Profile
        fields = [
         "image",
         "car_year",
         "car_make",
         "car_model",
         "current_mileage",
         "last_oil_change",
         "last_tire_maintenance",
         "last_fluid_check",
         "tire_company",
         "oil_change_company",
]
        
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "car_make": forms.Select(attrs={"class": "form-select", "id": "car-make"}),
            "car_model": forms.Select(attrs={"class": "form-select", "id": "car-model"}),
            "last_oil_change": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "last_tire_maintenance": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "last_fluid_check": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "current_mileage": forms.NumberInput(
                attrs={
            "class": "form-control",
            "placeholder": "Current vehicle mileage"
    }
),

"tire_company": forms.TextInput(
    attrs={"class": "form-control"}
),

"oil_change_company": forms.TextInput(
    attrs={"class": "form-control"}
),
        }

    def __init__(self, *args, **kwargs):
        make_choices = kwargs.pop("make_choices", [])
        model_choices = kwargs.pop("model_choices", [])
        super().__init__(*args, **kwargs)

        current_year = datetime.now().year + 1
        year_choices = [("", "Select Year")] + [
            (year, year) for year in range(current_year, 1980, -1)
        ]
        self.fields["car_year"].choices = year_choices
        self.fields["car_year"].widget.attrs.update(
            {"class": "form-select", "id": "id_car_year"}
        )

        self.fields["car_make"].choices = [("", "Select Make")] + list(make_choices)
        self.fields["car_model"].choices = [("", "Select Model")] + list(model_choices)

        self.fields["car_make"].required = False
        self.fields["car_model"].required = False

class MaintenanceRecordForm(forms.ModelForm):

    class Meta:
        model = MaintenanceRecord

        fields = [
            "maintenance_type",
            "custom_type",
            "service_date",
            "next_due_date",
            "mileage_at_service",
            "company_name",
            "notes",
        ]

        widgets = {

            "maintenance_type": forms.Select(
                attrs={"class": "form-select"}
            ),

            "custom_type": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "service_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "next_due_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "mileage_at_service": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Mileage at time of service"
                }
            ),

            "company_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),
        }