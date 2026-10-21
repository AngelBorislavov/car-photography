from django.shortcuts import render
from django.shortcuts import redirect

from photos.forms import CarPhotoForm

# Create your views here.
def home_view(request):
    return render(request,'pages/home.html')

