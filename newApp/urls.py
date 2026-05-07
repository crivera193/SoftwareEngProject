from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="newApp/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit-profile"),
    path("dashboard-dictionary/", views.dashboard_dictionary, name="dashboard-dictionary"),
    path("diy-videos/", views.diy_videos, name="diy-videos"),
    path('api/car-makes/', views.api_car_makes, name='api_car_makes'),
    path('api/car-models/', views.api_car_models, name='api_car_models'),
]