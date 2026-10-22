from django.shortcuts import render
from django.shortcuts import redirect
from .models import Photographers
from .forms import PhotographersForm
# Create your views here.
def photographers_list(request):
    if request.method == "POST":
        form = PhotographersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("photographers")
    else:
        form = PhotographersForm()

    all_photographers = Photographers.objects.all()
    context = {"photographers": all_photographers, "form": form}
    return render(request, 'photographers/photographer_list.html', context)