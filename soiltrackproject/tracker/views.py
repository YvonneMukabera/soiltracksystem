 

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

def login_portal(request):
    return render(request, "login_portal.html")

def register_account(request):
    return render(request, "register_account.html")

def password_reset(request):
    return render(request, "password_reset.html")
 

def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

def admin_user_management(request):
    return render(request, "admin_user_management.html")

def admin_sensor_network(request):
    return render(request, "admin_sensor_network.html")

def admin_analytics(request):
    return render(request, "admin_analytics.html")

def admin_fields(request):
    return render(request, "admin_fields.html")

def admin_notifications(request):
    return render(request, "admin_notifications.html")

def admin_settings(request):
    return render(request, "admin_settings.html")

def admin_login(request):
    return render(request, "admin_login.html")

def admin_register(request):
    return render(request, "admin_register.html")

def admin_password_reset(request):
    return render(request, "admin_password_reset.html")