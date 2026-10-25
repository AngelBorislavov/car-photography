from django.shortcuts import redirect, render
from django.db.models import Avg, Count, Max, Q
from .models import CarPhoto
from .forms import CarPhotoForm
from ranking.forms import RatingForm

# Create your views here.
def gallery_views(request):
    all_photos = CarPhoto.objects.annotate(
        average_rating=Avg("ratings__score"),
        rating_count=Count("ratings"),
        current_rating=Max(
            "ratings__score",
            filter=Q(ratings__session_key=request.session.session_key),
        ),
    )
    return render(
        request,
        "photos/gallery.html",
        {"photos": all_photos, "rating_form": RatingForm()},
    )

def photo_upload(request):
    form = CarPhotoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("gallery")

    all_photos = CarPhoto.objects.all()
    context = {
        'form' : form,
        'photos': all_photos,
    }

    return render(request, "photos/gallery_form.html", context)
