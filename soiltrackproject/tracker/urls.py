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
    path("auth/login/", views.login_portal, name="login_portal"),
    path("auth/register/", views.register_account, name="register_account"),
    path("auth/password-reset/", views.password_reset, name="password_reset"),
    
    path("admin-portal/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-portal/users/", views.admin_user_management, name="admin_users"),
    path("admin-portal/sensors/", views.admin_sensor_network, name="admin_sensors"),
    path("admin-portal/analytics/", views.admin_analytics, name="admin_analytics"),
    path("admin-portal/fields/", views.admin_fields, name="admin_fields"),
    path("admin-portal/notifications/", views.admin_notifications, name="admin_notifications"),
    path("admin-portal/settings/", views.admin_settings, name="admin_settings"),
    path("admin-auth/login/", views.admin_login, name="admin_login"),
    path("admin-auth/register/", views.admin_register, name="admin_register"),
    path("admin-auth/password-reset/", views.admin_password_reset, name="admin_password_reset"),
]
