from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from photographers.models import Photographers
from photos.models import Car, CarPhoto
from .models import Rating


class RatingTests(TestCase):
	def setUp(self):
		photographer = Photographers.objects.create(
			name="Test photographer",
			email="test@example.com",
			biography="Test",
		)
		self.car = Car.objects.create(brand="Test", model="Car")
		self.photo = CarPhoto.objects.create(
			photographer=photographer,
			title="Test photo",
			photo="test.jpg",
		)
		self.photo.cars.add(self.car)

	def test_rating_is_saved_and_updated_for_same_session(self):
		first_response = self.client.post(
			f"/gallery/{self.photo.pk}/rate/", {"score": "4"}
		)
		self.assertRedirects(first_response, "/gallery/")
		self.assertEqual(Rating.objects.get(photo=self.photo).score, 4)

		second_response = self.client.post(
			f"/gallery/{self.photo.pk}/rate/", {"score": "2"}
		)
		self.assertRedirects(second_response, "/gallery/")
		self.assertEqual(Rating.objects.filter(photo=self.photo).count(), 1)
		self.assertEqual(Rating.objects.get(photo=self.photo).score, 2)

	def test_invalid_score_is_not_saved(self):
		self.client.post(f"/gallery/{self.photo.pk}/rate/", {"score": "6"})
		self.assertFalse(Rating.objects.exists())

	def test_another_session_can_rate_same_photo(self):
		self.client.post(f"/gallery/{self.photo.pk}/rate/", {"score": "5"})
		another_client = self.client_class()
		another_client.post(f"/gallery/{self.photo.pk}/rate/", {"score": "3"})
		self.assertEqual(Rating.objects.filter(photo=self.photo).count(), 2)

	def test_gallery_shows_average_and_count(self):
		self.client.post(f"/gallery/{self.photo.pk}/rate/", {"score": "4"})
		response = self.client.get("/gallery/")
		self.assertEqual(response.status_code, 200)
		photo = response.context["photos"][0]
		self.assertEqual(photo.average_rating, 4)
		self.assertEqual(photo.rating_count, 1)

	def test_rank_list_only_shows_photos_from_last_week(self):
		old_photo = CarPhoto.objects.create(
			photographer=self.photo.photographer,
			title="Old photo",
			photo="old.jpg",
		)
		old_photo.cars.add(self.car)
		CarPhoto.objects.filter(pk=old_photo.pk).update(
			created_at=timezone.now() - timedelta(days=8)
		)

		response = self.client.get("/rank_list")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			list(response.context["photos_with_ratings"]),
			[self.photo],
		)
