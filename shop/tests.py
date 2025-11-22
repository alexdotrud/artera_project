from django.test import TestCase
from django.urls import reverse

from .models import Artwork, Category
from decimal import Decimal


class ShopBasicTests(TestCase):
    """Basic tests for the shop app views."""
    def setUp(self):
        # Create a category
        self.category = Category.objects.create(
            name="Minimal",
            friendly_name="Minimal"
        )

        # Create an artwork – adjust fields if your model needs more
        self.artwork = Artwork.objects.create(
            name="Test Artwork",
            description="Test description",
            price=Decimal("10.00"),
            category=self.category,
        )

    def test_all_artworks_view_returns_200(self):
        """all_artworks should load and list artworks."""
        url = reverse("all_artworks")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shop/list.html")
        self.assertContains(response, "Test Artwork")

    def test_artwork_detail_view_returns_200(self):
        """artwork_detail should load a single artwork page."""
        url = reverse("detail", args=[self.artwork.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shop/detail.html")
        self.assertContains(response, "Test Artwork")
        self.assertContains(response, "Test description")
