from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car_year = models.PositiveIntegerField(null=True, blank=True)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    vehicle_image_url = models.URLField(blank=True)
    current_mileage = models.PositiveIntegerField(null=True, blank=True)

    last_oil_change = models.DateField(null=True, blank=True)
    last_tire_maintenance = models.DateField(null=True, blank=True)
    last_fluid_check = models.DateField(null=True, blank=True)

    @property
    def next_oil_change(self):
        if self.last_oil_change:
            return self.last_oil_change + timedelta(days=180)
        return None

    @property
    def oil_change_status(self):
        if not self.last_oil_change:
            return "No Date"

        next_date = self.next_oil_change
        today = timezone.now().date()

        if next_date < today:
            return "Overdue"
        elif (next_date - today).days <= 14:
            return "Due Soon"
        return "Good"

    @property
    def next_tire_maintenance(self):
        if self.last_tire_maintenance:
            return self.last_tire_maintenance + timedelta(days=180)
        return None

    @property
    def tire_maintenance_status(self):
        if not self.last_tire_maintenance:
            return "No Date"

        next_date = self.next_tire_maintenance
        today = timezone.now().date()

        if next_date < today:
            return "Overdue"
        elif (next_date - today).days <= 14:
            return "Due Soon"
        return "Good"

    @property
    def next_fluid_check(self):
        if self.last_fluid_check:
            return self.last_fluid_check + timedelta(days=30)
        return None

    @property
    def fluid_check_status(self):
        if not self.last_fluid_check:
            return "No Date"

        next_date = self.next_fluid_check
        today = timezone.now().date()

        if next_date < today:
            return "Overdue"
        elif (next_date - today).days <= 7:
            return "Due Soon"
        return "Good"

    def __str__(self):
        return f"{self.user.username} Profile"


class MaintenanceRecord(models.Model):

    MAINTENANCE_CHOICES = [
        ("Oil Change", "Oil Change"),
        ("Tire Rotation", "Tire Rotation"),
        ("Brake Service", "Brake Service"),
        ("Battery Replacement", "Battery Replacement"),
        ("Air Filter", "Air Filter"),
        ("Coolant Flush", "Coolant Flush"),
        ("Transmission Service", "Transmission Service"),
        ("Other", "Other"),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="maintenance_records"
    )

    maintenance_type = models.CharField(
        max_length=100,
        choices=MAINTENANCE_CHOICES
    )

    custom_type = models.CharField(max_length=100, blank=True)
    service_date = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    mileage_at_service = models.PositiveIntegerField(null=True, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.maintenance_type == "Other":
            return self.custom_type

        return self.maintenance_type

#Forum    
class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(upload_to="forum_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    liked_by = models.ManyToManyField(
        User,
        related_name="liked_forum_posts",
        blank=True
    )

    def total_likes(self):
        return self.liked_by.count()

    def __str__(self):
        return self.title
    
class ForumReply(models.Model):
    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.post.title}"