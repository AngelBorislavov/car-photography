from django.shortcuts import redirect, render
from .models import CarPhoto
from .forms import CarPhotoForm

# Create your views here.
def gallery_views(request):
    all_photos = CarPhoto.objects.all()
    return render(request, "photos/gallery.html", {"photos": all_photos})

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
