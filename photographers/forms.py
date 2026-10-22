from django import forms

from .models import Photographers


class PhotographersForm(forms.ModelForm):
    class Meta:
        model = Photographers
        fields = ["name", "email", "biography"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Photographer name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "biography": forms.Textarea(attrs={"placeholder": "Short biography"}),
        }