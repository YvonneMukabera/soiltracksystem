from django.db import models
from django.contrib.auth.models import User


class AdminProfile(models.Model):
    """
    Extra info for system admins.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile")
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=100, default="System Admin")

    def __str__(self):
        return self.full_name


class Cooperative(models.Model):
    """
    Cooperative where farmers belong.
    """
    name = models.CharField(max_length=150)
    admin = models.ForeignKey(
        AdminProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cooperatives",
    )
    district = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    cell = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.farmers.count()

    @property
    def field_count(self):
        return self.fields.count()


class Farmer(models.Model):
    """
    Farmers who are members of a cooperative.
    """
    STATUS_CHOICES = [
        ("active", "Active"),
        ("pending", "Pending fees"),
        ("inactive", "Inactive"),
    ]

    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        related_name="farmers",
    )
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=30, blank=True)
    village = models.CharField(max_length=100)
    main_crop = models.CharField(max_length=100, blank=True)
    farm_size_ha = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="active"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class FieldPlot(models.Model):
    """
    Fields owned by farmers inside a cooperative.
    """
    STATUS_CHOICES = [
        ("active", "Active"),
        ("harvest", "Ready for harvest"),
        ("rest", "Resting"),
    ]

    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        related_name="fields",
    )
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE,
        related_name="fields",
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    location_description = models.CharField(max_length=255, blank=True)
    size_ha = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    main_crop = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="active"
    )

    class Meta:
        db_table = "fields"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Sensor(models.Model):
    """
    Physical sensors installed on fields.
    """
    SENSOR_TYPE_CHOICES = [
        ("moisture", "Soil moisture"),
        ("temperature", "Soil temperature"),
        ("ph", "pH sensor"),
        ("npk", "NPK sensor"),
        ("weather", "Weather node"),
    ]

    field = models.ForeignKey(
        FieldPlot,
        on_delete=models.CASCADE,
        related_name="sensors",
    )
    sensor_id = models.CharField(max_length=50, unique=True)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPE_CHOICES)
    location_on_field = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    battery_level = models.PositiveIntegerField(default=100)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.sensor_id} ({self.get_sensor_type_display()})"


class SensorReading(models.Model):
    """
    Readings coming from sensors over time.
    """
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="readings",
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    ph = models.FloatField(null=True, blank=True)
    moisture = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    nitrogen = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    conductivity = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"Reading for {self.sensor} at {self.recorded_at}"


class AIInsight(models.Model):
    """
    AI analysis over a field + its sensor data.
    """
    field = models.ForeignKey(
        FieldPlot,
        on_delete=models.CASCADE,
        related_name="ai_insights",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField()
    suitability_score = models.PositiveIntegerField(
        help_text="0–100 overall score"
    )
    nutrient_score = models.PositiveIntegerField(null=True, blank=True)
    water_retention_score = models.PositiveIntegerField(null=True, blank=True)
    drainage_score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"AI Insight for {self.field} ({self.created_at.date()})"


class CropRecommendation(models.Model):
    """
    Recommended crops for a field based on AI insight.
    """
    field = models.ForeignKey(
        FieldPlot,
        on_delete=models.CASCADE,
        related_name="crop_recommendations",
    )
    ai_insight = models.ForeignKey(
        AIInsight,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recommendations",
    )
    crop_name = models.CharField(max_length=100)
    suitability_score = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    expected_yield = models.CharField(max_length=100, blank=True)
    season = models.CharField(max_length=50, blank=True)
    is_top_choice = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.crop_name} for {self.field}"