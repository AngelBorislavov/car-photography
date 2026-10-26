from datetime import timedelta
from django.db.models import Avg
from django.shortcuts import render
from django.utils import timezone
from photos.models import CarPhoto

# Create your views here.
def home_view(request):
    week_ago = timezone.now() - timedelta(days=7)
    weekly_favorite = CarPhoto.objects.filter(
        created_at__gte=week_ago,
        ratings__score__isnull=False,
    ).annotate(
        average_rating=Avg("ratings__score")
    ).order_by("-average_rating", "-created_at").first()

    return render(request, "pages/home.html", {"weekly_favorite": weekly_favorite})


def custom_404(request, exception):
    return render(request, "pages/404.html", status=404)

