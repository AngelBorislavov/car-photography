"""
URL configuration for car_photography project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages import views as page_views
from photographers import views as photographer_views
from photos import views as photos_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', page_views.home_view, name="home"),
    path('photographers/', photographer_views.photographers_list,name = "photographers"),
    path('gallery/', photos_views.gallery_views, name='gallery'),
    path('gallery/gallery_upload', photos_views.photo_upload, name='gallery_upload')
]
