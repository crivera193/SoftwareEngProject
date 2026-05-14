# newApp/forms.py

from datetime import datetime

from django import forms
from django.contrib.auth.models import User

from .models import Profile, MaintenanceRecord, ForumPost, ForumReply


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

    maintenance_record_type = forms.ChoiceField(
        choices=[("", "Do not add maintenance record")] + MaintenanceRecord.MAINTENANCE_CHOICES,
        required=False,
        label="Add Maintenance Record Optional",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    maintenance_service_date = forms.DateField(
        required=False,
        label="Maintenance Service Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Profile

        fields = [
            "car_year",
            "car_make",
            "car_model",
            "current_mileage",
            "last_oil_change",
            "last_tire_maintenance",
            "last_fluid_check",
        ]

        widgets = {
            "car_make": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "car-make"
                }
            ),

            "car_model": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "car-model"
                }
            ),

            "current_mileage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Current vehicle mileage"
                }
            ),

            "last_oil_change": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "last_tire_maintenance": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "last_fluid_check": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
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
            {
                "class": "form-select",
                "id": "id_car_year"
            }
        )

        self.fields["car_make"].choices = [("", "Select Make")] + list(make_choices)
        self.fields["car_model"].choices = [("", "Select Model")] + list(model_choices)

        self.fields["car_make"].required = False
        self.fields["car_model"].required = False

    def clean(self):
        cleaned_data = super().clean()

        maintenance_record_type = cleaned_data.get("maintenance_record_type")
        maintenance_service_date = cleaned_data.get("maintenance_service_date")

        if maintenance_record_type and not maintenance_service_date:
            self.add_error(
                "maintenance_service_date",
                "Please enter a service date if adding a maintenance record."
            )

        return cleaned_data


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost

        fields = ["title", "content", "image"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg bg-white text-dark",
                    "placeholder": "Example: Why is my car shaking at 40 mph?"
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control bg-white text-dark",
                    "rows": 5,
                    "placeholder": "Describe your car issue or question..."
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control bg-white text-dark",
                    "accept": "image/*"
                }
            ),
        }


class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply

        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control forum-reply-input",
                    "rows": 2,
                    "placeholder": "Write a reply..."
                }
            ),
        }