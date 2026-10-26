from datetime import timedelta
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
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

def rank_list(request):
	week_ago = timezone.now() - timedelta(days=7)
	photos_with_ratings = CarPhoto.objects.filter(
		created_at__gte=week_ago
	).annotate(
		average_rating=Avg("ratings__score")
	).order_by("-average_rating", "-created_at")[:10]

	context = {
		'photos_with_ratings': photos_with_ratings,
	}
	return render(request, 'ranking/rank_list.html', context)
