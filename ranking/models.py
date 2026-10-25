from django.db import models
from django.db.models import Q
from photos.models import CarPhoto


class Rating(models.Model):
	photo = models.ForeignKey(CarPhoto, on_delete=models.CASCADE, related_name="ratings")
	session_key = models.CharField(max_length=40)
	score = models.PositiveSmallIntegerField(
		choices=[(score, str(score)) for score in range(1, 6)]
	)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=["photo", "session_key"],
				name="unique_photo_rating_per_session",
			),
			models.CheckConstraint(
				condition=Q(score__gte=1) & Q(score__lte=5),
				name="rating_score_between_1_and_5",
			),
		]

	def __str__(self):
		return f"{self.score}/5 for {self.photo}"
