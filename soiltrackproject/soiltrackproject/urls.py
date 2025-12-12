from django.contrib import admin
from django.urls import path
from tracker import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),
    path("ai-insights/", views.ai_insights, name="ai_insights"),
    path("sensors/", views.sensor_page, name="sensor"),
    path("history/", views.history, name="history"),
    path("crops/", views.crops, name="crops"),
]