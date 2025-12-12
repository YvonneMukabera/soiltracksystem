from django import forms
from .models import Farmer

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ["full_name", "phone_number", "village", "main_crop", "farm_size_ha", "status"]