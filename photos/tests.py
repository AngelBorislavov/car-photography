from django.test import TestCase
from django.urls import reverse
from photographers.models import Photographers
from .models import Car, CarPhoto


class PhotoDeletionTests(TestCase):
	def setUp(self):
		photographer = Photographers.objects.create(
			name="Test photographer",
			email="test@example.com",
			biography="Test",
		)
		self.car = Car.objects.create(
			brand="Test",
			model="Car",
			body_type="coupe",
		)
		self.photo = CarPhoto.objects.create(
			photographer=photographer,
			title="Test photo",
			photo="test.jpg",
		)
		self.photo.cars.add(self.car)
		self.other_photographer = Photographers.objects.create(
			name="Another photographer",
			email="another@example.com",
			biography="Another test photographer",
		)

	def test_photographer_gallery_shows_only_their_photos(self):
		other_photo = CarPhoto.objects.create(
			photographer=self.other_photographer,
			title="Other photo",
			photo="other.jpg",
		)
		other_photo.cars.add(self.car)

		response = self.client.get(
			reverse("photographer_photos", args=[self.photo.photographer_id])
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context["photos"]), [self.photo])
		self.assertNotContains(response, "Other photo")
		self.assertTrue(CarPhoto.objects.filter(pk=other_photo.pk).exists())

	def test_post_deletes_photo_and_redirects_to_gallery(self):
		response = self.client.post(reverse("delete_photo", args=[self.photo.pk]))

		self.assertRedirects(response, reverse("gallery"))
		self.assertFalse(CarPhoto.objects.filter(pk=self.photo.pk).exists())

	def test_get_shows_confirmation_without_deleting_photo(self):
		response = self.client.get(reverse("delete_photo", args=[self.photo.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "photos/gallery_delete.html")
		self.assertContains(response, "Delete Test photo?")
		self.assertTrue(CarPhoto.objects.filter(pk=self.photo.pk).exists())

	def test_upload_form_can_create_and_connect_a_car(self):
		from io import BytesIO
		from django.core.files.uploadedfile import SimpleUploadedFile
		from django.test import override_settings
		from PIL import Image
		import tempfile

		image_content = BytesIO()
		Image.new("RGB", (1, 1), color="white").save(image_content, format="JPEG")
		with tempfile.TemporaryDirectory() as media_dir, override_settings(MEDIA_ROOT=media_dir):
			response = self.client.post(
				reverse("gallery_upload"),
				{
					"title": "New car photo",
					"photographer": self.photo.photographer_id,
					"cars": [self.car.pk],
					"new_car_brand": "Mazda",
					"new_car_model": "MX-5",
					"new_car_body_type": "convertible",
					"photo": SimpleUploadedFile(
						"mx5.jpg", image_content.getvalue(), content_type="image/jpeg"
					),
				},
			)

		self.assertRedirects(response, reverse("gallery"))
		new_photo = CarPhoto.objects.get(title="New car photo")
		self.assertEqual(new_photo.photographer_id, self.photo.photographer_id)
		self.assertEqual(new_photo.cars.count(), 2)
		new_car = new_photo.cars.get(brand="Mazda")
		self.assertEqual(str(new_car), "Mazda MX-5")
		self.assertEqual(new_car.body_type, "convertible")

	def test_photo_detail_displays_associated_cars(self):
		response = self.client.get(reverse("photo_detail", args=[self.photo.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Test Car")
		self.assertContains(response, "Coupe")

	def test_upload_form_shows_existing_cars(self):
		response = self.client.get(reverse("gallery_upload"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Cars in the photo")
		self.assertContains(response, "Test Car")

	def test_gallery_search_matches_car_brand_or_model(self):
		response = self.client.get(reverse("gallery"), {"q": "Car"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context["photos"]), [self.photo])

	def test_gallery_search_hides_nonmatching_photos(self):
		response = self.client.get(reverse("gallery"), {"q": "Toyota"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context["photos"]), [])

	def test_edit_photo_updates_title_and_car_links(self):
		response = self.client.post(
			reverse("edit_photo", args=[self.photo.pk]),
			{
				"photographer": self.photo.photographer_id,
				"title": "Updated title",
				"cars": [self.car.pk],
			},
		)

		self.assertRedirects(response, reverse("gallery"))
		self.photo.refresh_from_db()
		self.assertEqual(self.photo.title, "Updated title")
		self.assertEqual(list(self.photo.cars.all()), [self.car])

	def test_edit_photo_page_prepopulates_existing_values(self):
		response = self.client.get(reverse("edit_photo", args=[self.photo.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Edit photo")
		self.assertContains(response, "Test photo")
		self.assertContains(response, "Test Car")
