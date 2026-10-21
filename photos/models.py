from django.db import models

# Create your models here.
class CarPhoto(models.Model):
    author = models.CharField(max_length=20)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=20)
    photo = models.ImageField()
