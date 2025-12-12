from django.shortcuts import render
from django.db.models import Count, Max, Avg
from .models import (
    Cooperative,
    Farmer,
    FieldPlot,
    Sensor,
    SensorReading,
    AIInsight,
    CropRecommendation,
)


# =========================
# HOME DASHBOARD
# =========================
def home(request):
    """
    Main dashboard page.
    Shows high-level statistics about the system + latest field reading.
    """

    total_coops = Cooperative.objects.count()
    total_farmers = Farmer.objects.count()
    total_fields = FieldPlot.objects.count()
    total_sensors = Sensor.objects.count()
    total_readings = SensorReading.objects.count()
    total_insights = AIInsight.objects.count()
    total_recommendations = CropRecommendation.objects.count()

    fields = FieldPlot.objects.all().order_by("name")

    latest_reading = (
        SensorReading.objects
        .select_related("sensor", "sensor__field", "sensor__field__cooperative")
        .order_by("-recorded_at")
        .first()
    )

    context = {
        "total_coops": total_coops,
        "total_farmers": total_farmers,
        "total_fields": total_fields,
        "total_sensors": total_sensors,
        "total_readings": total_readings,
        "total_insights": total_insights,
        "total_recommendations": total_recommendations,
        "fields": fields,
        "latest_reading": latest_reading,
    }
    return render(request, "tracker/home.html", context)


# =========================
# AI INSIGHTS PAGE
# =========================
def ai_insights(request):
    """
    Page showing AI insights + crop recommendations.
    Optional filters: ?coop=<id>&field=<id>
    """

    coop_id = request.GET.get("coop")
    field_id = request.GET.get("field")

    insights_qs = (
        AIInsight.objects
        .select_related("field", "field__cooperative", "field__farmer")
        .order_by("-created_at")
    )

    if coop_id:
        insights_qs = insights_qs.filter(field__cooperative_id=coop_id)

    if field_id:
        insights_qs = insights_qs.filter(field_id=field_id)

    recommendations_qs = (
        CropRecommendation.objects
        .select_related("field", "field__cooperative")
        .order_by("-suitability_score")
    )

    if coop_id:
        recommendations_qs = recommendations_qs.filter(field__cooperative_id=coop_id)

    if field_id:
        recommendations_qs = recommendations_qs.filter(field_id=field_id)

    context = {
        "insights": insights_qs,
        "recommendations": recommendations_qs,
        "cooperatives": Cooperative.objects.all().order_by("name"),
        "fields": FieldPlot.objects.all().order_by("name"),
        "selected_coop_id": coop_id,
        "selected_field_id": field_id,
    }
    return render(request, "tracker/ai_insights.html", context)


# =========================
# SENSORS PAGE
# =========================
def sensor_page(request):
    """
    Sensors page – summary per sensor using readings reverse relation.
    """

    sensors = (
        Sensor.objects
        .select_related("field", "field__cooperative")
        .annotate(
            reading_count=Count("readings"),                  # how many readings
            last_seen_at=Max("readings__recorded_at"),        # last reading time
            avg_ph=Avg("readings__ph"),                       # average pH
            avg_moisture=Avg("readings__moisture"),           # average moisture
            avg_temperature=Avg("readings__temperature"),     # average temperature
        )
        .order_by("-last_seen_at")
    )

    context = {
        "sensors": sensors,
    }
    return render(request, "tracker/sensors.html", context)


# =========================
# HISTORY PAGE
# =========================
def history(request):
    """
    Historical data page.
    Shows recent sensor readings, with optional filters.
    """

    coop_id = request.GET.get("coop")
    field_id = request.GET.get("field")
    sensor_id = request.GET.get("sensor")

    readings_qs = (
        SensorReading.objects
        .select_related("sensor", "sensor__field", "sensor__field__cooperative")
        .order_by("-recorded_at")
    )

    if coop_id:
        readings_qs = readings_qs.filter(sensor__field__cooperative_id=coop_id)

    if field_id:
        readings_qs = readings_qs.filter(sensor__field_id=field_id)

    if sensor_id:
        readings_qs = readings_qs.filter(sensor_id=sensor_id)

    readings_qs = readings_qs[:200]

    context = {
        "readings": readings_qs,
        "cooperatives": Cooperative.objects.all().order_by("name"),
        "fields": FieldPlot.objects.all().order_by("name"),
        "sensors": Sensor.objects.all().order_by("sensor_id"),
        "selected_coop_id": coop_id,
        "selected_field_id": field_id,
        "selected_sensor_id": sensor_id,
    }
    return render(request, "tracker/history.html", context)


# =========================
# CROPS PAGE
# =========================
def crops(request):
    """
    Crops / crop recommendations page.
    Shows recommended crops per field, with optional filters.
    """

    coop_id = request.GET.get("coop")
    field_id = request.GET.get("field")
    season = request.GET.get("season")

    recs_qs = (
        CropRecommendation.objects
        .select_related("field", "field__cooperative")
        .order_by("-suitability_score")
    )

    if coop_id:
        recs_qs = recs_qs.filter(field__cooperative_id=coop_id)

    if field_id:
        recs_qs = recs_qs.filter(field_id=field_id)

    if season:
        recs_qs = recs_qs.filter(season=season)

    top_choices = recs_qs.filter(is_top_choice=True)

    context = {
        "recommendations": recs_qs,
        "top_choices": top_choices,
        "cooperatives": Cooperative.objects.all().order_by("name"),
        "fields": FieldPlot.objects.all().order_by("name"),
        "selected_coop_id": coop_id,
        "selected_field_id": field_id,
        "selected_season": season,
    }
    return render(request, "tracker/crops.html", context)


# =========================
# COOPERATIVES PAGE
# =========================
def cooperatives(request):
    """
    Cooperative overview page.
    Uses the special cooperative template (its own navbar, not base.html).
    """

    coop_qs = (
        Cooperative.objects
        .annotate(
            farmer_count=Count("farmer"),
            field_count=Count("fieldplot"),
        )
        .order_by("name")
    )

    current_coop = coop_qs.first()

    members = Farmer.objects.none()
    fields = FieldPlot.objects.none()
    if current_coop:
        members = Farmer.objects.filter(cooperative=current_coop).order_by("full_name")
        fields = FieldPlot.objects.filter(cooperative=current_coop).order_by("name")

    context = {
        "cooperatives": coop_qs,
        "current_coop": current_coop,
        "members": members,
        "fields": fields,
    }
    return render(request, "tracker/cooperatives.html", context)