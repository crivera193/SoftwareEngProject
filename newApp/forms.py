from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image',
            'car_owned',
            'car_type',
            'car_make',
            'car_model',
            'last_oil_change',
            'last_tire_maintenance',
            'last_fluid_check',
        ]

        labels = {
            'image': 'Profile Picture',
            'car_owned': 'Do you own a car?',
            'car_type': 'Type of Car',
            'car_make': 'Make',
            'car_model': 'Model',
            'last_oil_change': 'Last Oil Change',
            'last_tire_maintenance': 'Last Tire Maintenance',
            'last_fluid_check': 'Last Fluid Check',
        }

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'car_owned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'car_type': forms.TextInput(attrs={'class': 'form-control'}),
            'car_make': forms.TextInput(attrs={'class': 'form-control'}),
            'car_model': forms.TextInput(attrs={'class': 'form-control'}),
            'last_oil_change': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'last_tire_maintenance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'last_fluid_check': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }