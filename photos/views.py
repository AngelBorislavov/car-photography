from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg, Count, Max, Q
from django.views.decorators.http import require_POST
from photographers.models import Photographers
from .models import Car, CarPhoto
from .forms import CarPhotoForm
from ranking.forms import RatingForm

# Create your views here.
def gallery_views(request):
    search_query = request.GET.get("q", "").strip()
    all_photos = CarPhoto.objects.prefetch_related("cars")
    if search_query:
        all_photos = all_photos.filter(
            Q(cars__brand__icontains=search_query)
            | Q(cars__model__icontains=search_query)
        ).distinct()

    all_photos = all_photos.annotate(
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
        {
            "photos": all_photos,
            "rating_form": RatingForm(),
            "search_query": search_query,
        },
    )

def photographer_gallery(request, photographer_id):
    photographer = get_object_or_404(Photographers, pk=photographer_id)
    search_query = request.GET.get("q", "").strip()
    photographer_photos = CarPhoto.objects.filter(
        photographer=photographer
    ).prefetch_related("cars")
    if search_query:
        photographer_photos = photographer_photos.filter(
            Q(cars__brand__icontains=search_query)
            | Q(cars__model__icontains=search_query)
        ).distinct()

    photographer_photos = photographer_photos.annotate(
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
        {
            "photos": photographer_photos,
            "rating_form": RatingForm(),
            "photographer": photographer,
            "search_query": search_query,
        },
    )


def photo_detail(request, photo_id):
    photo = get_object_or_404(
        CarPhoto.objects.select_related("photographer").prefetch_related("cars"),
        pk=photo_id,
    )
    return render(request, "photos/photo_detail.html", {"photo": photo})


def photo_upload(request):
    form = CarPhotoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("gallery")

    context = {
        "form": form,
        "cars": Car.objects.all(),
    }

    return render(request, "photos/gallery_form.html", context)


def edit_photo(request, photo_id):
    photo = get_object_or_404(CarPhoto, pk=photo_id)
    form = CarPhotoForm(request.POST or None, request.FILES or None, instance=photo)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "The photo has been updated successfully.")
        return redirect("gallery")

    return render(
        request,
        "photos/gallery_form.html",
        {"form": form, "photo": photo, "is_edit": True},
    )


def delete_photo(request, photo_id):
    photo = get_object_or_404(CarPhoto, pk=photo_id)
    if request.method == "POST":
        photo_file = photo.photo
        photo.delete()
        if photo_file:
            photo_file.delete(save=False)
        return redirect("gallery")

    messages.success(request, "The photo has been deleted successfully.")
    return render(request, "photos/gallery_delete.html", {"photo": photo})

