from django.contrib import admin
from django.urls import path
from tracker import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # home dashboard
    path("", views.home, name="home"),

    # AI insights page
    path("ai-insights/", views.ai_insights, name="ai_insights"),

    # sensors page (note: view function name = sensor_page, URL name = "sensor")
    path("sensors/", views.sensor_page, name="sensor"),

    # history page
    path("history/", views.history, name="history"),

    # crops page
    path("crops/", views.crops, name="crops"),

    # cooperative page
    path("cooperatives/", views.cooperatives, name="cooperatives"),
]