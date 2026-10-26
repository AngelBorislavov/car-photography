from django.test import TestCase, override_settings
from django.utils import timezone
from datetime import timedelta
from photographers.models import Photographers
from photos.models import Car, CarPhoto
from ranking.models import Rating


class HomeWeeklyFavoriteTests(TestCase):
	def setUp(self):
		self.photographer = Photographers.objects.create(
			name="Test photographer",
			email="test@example.com",
			biography="Test biography",
		)
		self.car = Car.objects.create(brand="Test", model="Car")

	def make_photo(self, title):
		photo = CarPhoto.objects.create(
			photographer=self.photographer,
			title=title,
			photo=f"{title}.jpg",
		)
		photo.cars.add(self.car)
		return photo

	def test_home_shows_highest_rated_photo_uploaded_this_week(self):
		favorite = self.make_photo("Weekly favorite")
		other_recent = self.make_photo("Other recent photo")
		old_photo = self.make_photo("Old photo")
		CarPhoto.objects.filter(pk=old_photo.pk).update(
			created_at=timezone.now() - timedelta(days=8)
		)
		Rating.objects.create(photo=favorite, session_key="first", score=5)
		Rating.objects.create(photo=other_recent, session_key="second", score=3)
		Rating.objects.create(photo=old_photo, session_key="third", score=5)

		response = self.client.get("/")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["weekly_favorite"], favorite)


class CustomNotFoundPageTests(TestCase):
	@override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
	def test_unknown_url_uses_custom_404_template(self):
		response = self.client.get("/this-page-does-not-exist/")

		self.assertEqual(response.status_code, 404)
		self.assertTemplateUsed(response, "pages/404.html")
		self.assertContains(response, "Page not found", status_code=404)
