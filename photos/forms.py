from django import forms

from .models import Car, CarPhoto
from photographers.models import Photographers


class CarPhotoForm(forms.ModelForm):
	created_at = forms.DateTimeField(
		required=False,
		disabled=True,
		label="Uploaded at",
	)
	photographer = forms.ModelChoiceField(
		queryset=Photographers.objects.none(),
		required=True,
		label="Photographer",
	)
	cars = forms.ModelMultipleChoiceField(
		queryset=Car.objects.none(),
		required=False,
		label="Cars in this photo",
		widget=forms.CheckboxSelectMultiple,
	)
	new_car_brand = forms.CharField(
		required=False,
		max_length=50,
		label="New car brand",
		widget=forms.TextInput(attrs={"placeholder": "e.g. BMW"}),
	)
	new_car_model = forms.CharField(
		required=False,
		max_length=50,
		label="New car model",
		widget=forms.TextInput(attrs={"placeholder": "e.g. M3"}),
	)
	new_car_body_type = forms.ChoiceField(
		required=False,
		label="Body type",
		choices=[("", "Choose a body type")] + Car.BODY_TYPE_CHOICES,
	)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["photographer"].queryset = Photographers.objects.all()
		self.fields["cars"].queryset = Car.objects.all()
		if self.instance.pk:
			self.initial["created_at"] = self.instance.created_at

	def clean(self):
		cleaned_data = super().clean()
		new_brand = cleaned_data.get("new_car_brand", "").strip()
		new_model = cleaned_data.get("new_car_model", "").strip()
		selected_cars = cleaned_data.get("cars")

		if bool(new_brand) != bool(new_model):
			self.add_error(
				"new_car_model" if new_brand else "new_car_brand",
				"Enter both the brand and model to add a car.",
			)
		if not selected_cars and not (new_brand and new_model):
			self.add_error("cars", "Select an existing car or enter a new car below.")
		return cleaned_data

	class Meta:
		model = CarPhoto
		fields = ["photographer", "title", "photo", "cars"]
		labels = {"title": "Photo title", "photo": "Photo file"}
		help_texts = {"cars": "Select every car visible in this photo."}

	def save(self, commit=True):
		photo = super().save(commit=commit)
		if commit:
			self.save_new_car(photo)
		return photo

	def save_new_car(self, photo):
		brand = self.cleaned_data.get("new_car_brand", "").strip()
		model = self.cleaned_data.get("new_car_model", "").strip()
		if brand and model:
			car, _ = Car.objects.get_or_create(
				brand=brand,
				model=model,
				defaults={"body_type": self.cleaned_data.get("new_car_body_type") or "other"},
			)
			photo.cars.add(car)

