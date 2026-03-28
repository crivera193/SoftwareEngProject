from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    car_owned = models.BooleanField(default=False)
    car_type = models.CharField(max_length=100, blank=True)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)

    last_oil_change = models.DateField(null=True, blank=True)
    last_tire_maintenance = models.DateField(null=True, blank=True)
    last_fluid_check = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def next_oil_change(self):
        if self.last_oil_change:
            return self.last_oil_change + timedelta(days=90)
        return None

    def next_tire_maintenance(self):
        if self.last_tire_maintenance:
            return self.last_tire_maintenance + timedelta(days=180)
        return None

    def next_fluid_check(self):
        if self.last_fluid_check:
            return self.last_fluid_check + timedelta(days=30)
        return None

    def oil_change_status(self):
        next_date = self.next_oil_change()
        if not next_date:
            return "No date entered"

        today = timezone.now().date()
        if next_date < today:
            return "Overdue"
        elif next_date <= today + timedelta(days=7):
            return "Due soon"
        return "Up to date"

    def tire_maintenance_status(self):
        next_date = self.next_tire_maintenance()
        if not next_date:
            return "No date entered"

        today = timezone.now().date()
        if next_date < today:
            return "Overdue"
        elif next_date <= today + timedelta(days=14):
            return "Due soon"
        return "Up to date"

    def fluid_check_status(self):
        next_date = self.next_fluid_check()
        if not next_date:
            return "No date entered"

        today = timezone.now().date()
        if next_date < today:
            return "Overdue"
        elif next_date <= today + timedelta(days=7):
            return "Due soon"
        return "Up to date"