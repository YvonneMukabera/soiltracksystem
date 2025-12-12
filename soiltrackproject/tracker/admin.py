from django.contrib import admin
from .models import (
    AdminProfile,
    Cooperative,
    Farmer,
    FieldPlot,
    Sensor,
    SensorReading,
    AIInsight,
    CropRecommendation,
)


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", "role", "user")


@admin.register(Cooperative)
class CooperativeAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "sector", "member_count", "field_count")


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "cooperative", "village", "main_crop", "farm_size_ha", "status")
    list_filter = ("cooperative", "status", "village")


@admin.register(FieldPlot)
class FieldPlotAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "cooperative", "farmer", "size_ha", "main_crop", "status")
    list_filter = ("cooperative", "status", "main_crop")


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("sensor_id", "sensor_type", "field", "is_active", "battery_level", "last_seen")
    list_filter = ("sensor_type", "is_active")


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ("sensor", "recorded_at", "ph", "moisture", "temperature")
    list_filter = ("sensor__sensor_type",)


@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ("field", "created_at", "suitability_score")
    list_filter = ("field__cooperative",)


@admin.register(CropRecommendation)
class CropRecommendationAdmin(admin.ModelAdmin):
    list_display = ("crop_name", "field", "suitability_score", "is_top_choice", "season")
    list_filter = ("is_top_choice", "season", "field__cooperative")