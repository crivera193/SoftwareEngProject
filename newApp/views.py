# newApp/views.py

import json
import requests
from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import URLError, HTTPError

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import UserUpdateForm, ProfileUpdateForm

VPIC_BASE_URL = "https://vpic.nhtsa.dot.gov/api/vehicles"


def home(request):
    return render(request, "newApp/home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created. You can now log in.")
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(request, "newApp/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "newApp/profile.html")


def dashboard_dictionary(request):
    return render(request, "newApp/dashboard_dictionary.html")


def diy_videos(request):
    return render(request, "newApp/diy_videos.html")


def fetch_json(url):
    try:
        with urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    except (URLError, HTTPError, TimeoutError, ValueError):
        return {"Results": []}


def get_car_makes():
    url = f"{VPIC_BASE_URL}/GetMakesForVehicleType/car?format=json"
    data = fetch_json(url)

    makes = []

    for item in data.get("Results", []):
        make_name = item.get("MakeName", "").strip()

        if make_name:
            makes.append((make_name, make_name))

    return sorted(set(makes), key=lambda x: x[0].lower())


def get_car_models(make, year):
    if not make or not year:
        return []

    safe_make = quote(str(make).strip())
    safe_year = quote(str(year).strip())

    url = (
        f"{VPIC_BASE_URL}/GetModelsForMakeYear/"
        f"make/{safe_make}/modelyear/{safe_year}?format=json"
    )

    data = fetch_json(url)

    models = []

    for item in data.get("Results", []):
        model_name = item.get("Model_Name", "").strip()

        if model_name:
            models.append((model_name, model_name))

    return sorted(set(models), key=lambda x: x[0].lower())


def get_vehicle_image(year, make, model):
    query = f"{year} {make} {model} car"

    url = "https://api.unsplash.com/search/photos"

    headers = {
        "Accept-Version": "v1",
    }

    params = {
        "query": query,
        "per_page": 1,
        "client_id": "sz9DIWRV3xQh9FevRdtdl7IypqTLw_syfNcly4Hvav4",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        data = response.json()
        results = data.get("results", [])

        if results:
            return results[0]["urls"]["regular"]

    except Exception:
        pass

    return ""


@login_required
def edit_profile(request):
    make_choices = get_car_makes()

    existing_year = request.user.profile.car_year
    existing_make = request.user.profile.car_make
    existing_model = request.user.profile.car_model

    if request.method == "POST":
        posted_year = request.POST.get("car_year") or ""
        posted_make = request.POST.get("car_make") or ""

        if posted_year and posted_make:
            model_choices = get_car_models(posted_make, posted_year)
        else:
            model_choices = []

        u_form = UserUpdateForm(request.POST, instance=request.user)

        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
            make_choices=make_choices,
            model_choices=model_choices,
        )

        if u_form.is_valid() and p_form.is_valid():
            car_model = p_form.cleaned_data.get("car_model")

            if car_model:
                valid_models = {choice[0] for choice in model_choices}

                if car_model not in valid_models:
                    p_form.add_error(
                        "car_model",
                        "Please select a valid model for that make and year."
                    )

            if not p_form.errors:
                u_form.save()

                profile = p_form.save(commit=False)

                if profile.car_year and profile.car_make and profile.car_model:
                    profile.vehicle_image_url = get_vehicle_image(
                        profile.car_year,
                        profile.car_make,
                        profile.car_model
                    )

                profile.save()

                messages.success(request, "Your profile has been updated.")
                return redirect("profile")

    else:
        if existing_make and existing_year:
            model_choices = get_car_models(existing_make, existing_year)
        else:
            model_choices = []

        u_form = UserUpdateForm(instance=request.user)

        p_form = ProfileUpdateForm(
            instance=request.user.profile,
            make_choices=make_choices,
            model_choices=model_choices,
        )

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }

    return render(request, "newApp/edit_profile.html", context)


@login_required
def api_car_makes(request):
    makes = get_car_makes()

    return JsonResponse({
        "makes": [{"value": value, "label": label} for value, label in makes]
    })


@login_required
def api_car_models(request):
    year = request.GET.get("year")
    make = request.GET.get("make")

    if not year or not make:
        return JsonResponse({"models": []})

    models = get_car_models(make, year)

    return JsonResponse({
        "models": [{"value": value, "label": label} for value, label in models]
    })