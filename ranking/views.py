from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from photos.models import CarPhoto
from .forms import RatingForm
from .models import Rating

@require_POST
def rate_photo(request, photo_id):
	photo = get_object_or_404(CarPhoto, pk=photo_id)
	form = RatingForm(request.POST)
	if form.is_valid():
		if request.session.session_key is None:
			request.session.create()
		Rating.objects.update_or_create(
			photo=photo,
			session_key=request.session.session_key,
			defaults={"score": form.cleaned_data["score"]},
		)
	return redirect("gallery")
