 

# Create your views here.
from django.shortcuts import render

def landing(request):
    return render(request, "landing.html")

def learn_more(request):
    return render(request, "learn_more.html")    

def home(request):
    return render(request, "home.html")

def ai_insights(request):
    return render(request, "ai_insights.html")

def sensor(request):
    return render(request, "sensor.html")

def history(request):
    return render(request, "history.html")

def crops(request):
    return render(request, "crops.html")

def cooperatives(request):
    return render(request, "cooperatives.html")
