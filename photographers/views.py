from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .models import Photographers
from .forms import PhotographersForm
# Create your views here.
def photographers_list(request):
    all_photographers = Photographers.objects.all()
    context = {"photographers": all_photographers}
    return render(request, 'photographers/photographer_list.html', context)

def photographer_form(request):
    if request.method == "POST":
        form = PhotographersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The photographer has been added successfully.")
            return redirect("photographers")
    else:
        form = PhotographersForm()

    return render(request, "photographers/photographer_form.html", {"form": form})

def edit_photographer(request, photographer_id):
    photographer = get_object_or_404(Photographers, pk=photographer_id)
    form = PhotographersForm(request.POST or None, instance=photographer)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "The information about the photographer has been updated.")
        return redirect("photographers")

    return render(
        request,
        "photographers/photographer_edit.html",
        {"form": form, "photographer": photographer},
    )


@require_http_methods(["GET", "POST"])
def photographer_delete(request, photographer_id):
    photographer = get_object_or_404(Photographers, pk=photographer_id)
    if request.method == "POST":
        from photos.models import CarPhoto

        photo_files = [
            (photo.photo.storage, photo.photo.name)
            for photo in photographer.photos.all()
            if photo.photo
        ]
        with transaction.atomic():
            CarPhoto.objects.filter(photographer=photographer).delete()
            photographer.delete()
            for storage, name in photo_files:
                transaction.on_commit(
                    lambda storage=storage, name=name: storage.delete(name)
                )
        messages.success(request, "The photographer and their photos have been deleted successfully.")
        return redirect("photographers")

    return render(
        request,
        "photographers/photographer_delete.html",
        {
            "photographer": photographer,
            "photo_count": photographer.photos.count(),
        },
    )