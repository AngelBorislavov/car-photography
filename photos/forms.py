from django import forms

from .models import CarPhoto


class CarPhotoForm(forms.ModelForm):
	class Meta:
		model = CarPhoto
		fields = ["author", "brand","model", "photo"]

