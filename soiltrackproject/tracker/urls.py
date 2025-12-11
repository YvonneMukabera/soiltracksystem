# soiltrack_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("learn-more/", views.learn_more, name="learn_more"),
    path("home/", views.home, name="home"),
    path("ai-insights/", views.ai_insights, name="ai_insights"),
    path("sensor/", views.sensor, name="sensor"),
    path("history/", views.history, name="history"),
    path("crops/", views.crops, name="crops"),
    path("cooperatives/", views.cooperatives, name="cooperatives"),
]
