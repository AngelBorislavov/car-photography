from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from photographers.models import Photographers
from photos.models import Car, CarPhoto


class PhotographerManagementTests(TestCase):
	def setUp(self):
		self.photographer = Photographers.objects.create(
			name="Test photographer",
			email="test@example.com",
			biography="Test biography",
		)
		self.car = Car.objects.create(brand="Test", model="Car")

	def test_edit_photographer_updates_details(self):
		response = self.client.post(
			reverse("edit_photographer", args=[self.photographer.pk]),
			{
				"name": "Updated photographer",
				"email": "updated@example.com",
				"biography": "Updated biography",
			},
		)

		self.assertRedirects(response, reverse("photographers"))
		self.photographer.refresh_from_db()
		self.assertEqual(self.photographer.name, "Updated photographer")

	def test_delete_photographer_removes_record(self):
		response = self.client.post(
			reverse("delete_photographer", args=[self.photographer.pk])
		)

		self.assertRedirects(response, reverse("photographers"))
		self.assertFalse(Photographers.objects.filter(pk=self.photographer.pk).exists())

	def test_get_delete_page_shows_confirmation_without_deleting(self):
		photo = CarPhoto.objects.create(
			photographer=self.photographer,
			title="Test photo",
			photo="test.jpg",
		)
		photo.cars.add(self.car)
		response = self.client.get(
			reverse("delete_photographer", args=[self.photographer.pk])
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Delete Test photographer?")
		self.assertContains(response, "Deleting this photo will also delete 1 photos.")
		self.assertTrue(Photographers.objects.filter(pk=self.photographer.pk).exists())

	def test_delete_photographer_deletes_photos_and_files(self):
		photo = CarPhoto.objects.create(
			photographer=self.photographer,
			title="Test photo",
			photo=SimpleUploadedFile("test.jpg", b"test image data"),
		)
		photo.cars.add(self.car)
		photo_path = photo.photo.path
		self.assertTrue(photo.photo.storage.exists(photo.photo.name))

		with self.captureOnCommitCallbacks(execute=True):
			response = self.client.post(
				reverse("delete_photographer", args=[self.photographer.pk]),
				follow=True,
			)

		self.assertFalse(Photographers.objects.filter(pk=self.photographer.pk).exists())
		self.assertFalse(CarPhoto.objects.filter(pk=photo.pk).exists())
		self.assertFalse(photo.photo.storage.exists(photo.photo.name))
		self.assertContains(response, "The photographer and their photos have been deleted successfully.")
