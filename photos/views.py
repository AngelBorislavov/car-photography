from django.shortcuts import render

# Create your views here.
def photo_upload(request):
    form = CarPhotoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("upload")

    return render(request, "pages/upload.html", {"form": form})

def photo_list(request):
    