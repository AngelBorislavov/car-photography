from django.db import models
from photographers.models import Photographers

# Create your models here.
class CarPhoto(models.Model):
    photographer = models.ForeignKey(
        Photographers,
        on_delete=models.PROTECT,
        related_name="photos",
    )
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=20)
    photo = models.ImageField()

    def __srt__(self):
        return f'{self.title}'