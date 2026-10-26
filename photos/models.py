from django.db import models
from photographers.models import Photographers

# Create your models here.
class Car(models.Model):
    BODY_TYPE_CHOICES = [
        ("sedan", "Sedan"),
        ("hatchback", "Hatchback"),
        ("coupe", "Coupe"),
        ("suv", "SUV"),
        ("wagon", "Wagon"),
        ("convertible", "Convertible"),
        ("other", "Other"),
    ]

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    body_type = models.CharField(
        max_length=20, choices=BODY_TYPE_CHOICES, default="other"
    )

    class Meta:
        ordering = ["brand", "model"]
        constraints = [
            models.UniqueConstraint(
                fields=["brand", "model"], name="unique_car_brand_model"
            )
        ]

    def __str__(self):
        return f"{self.brand} {self.model}"


class CarPhoto(models.Model):
    photographer = models.ForeignKey(
        Photographers,
        on_delete=models.PROTECT,
        related_name="photos",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    photo = models.ImageField()
    cars = models.ManyToManyField(Car, blank=True, related_name="photos")

    def __str__(self):
        return f'{self.title}'