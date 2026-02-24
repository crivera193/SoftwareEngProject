from django.shortcuts import render

def home(request):
    return render(request, "newApp/home.html")
# Create your views here.
