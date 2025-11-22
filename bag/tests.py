from django.test import TestCase
from django.urls import reverse
from shop.models import Artwork


class BagBasicTests(TestCase):
    """Basic tests for adding and removing items from the bag."""
    def setUp(self):
        self.artwork = Artwork.objects.create(
            name="Test Artwork",
            price=10.00,
        )
        self.add_url = reverse("add_to_bag", args=[self.artwork.id])
        self.remove_url = reverse("remove_from_bag", args=[self.artwork.id])
        self.view_bag_url = reverse("view_bag")

    def test_add_to_bag(self):
        """Simple test: adding an item with size puts it in session."""
        self.client.post(
            self.add_url,
            {"product_size": "A4", "redirect_url": self.view_bag_url}
        )

        bag = self.client.session.get("bag", {})
        key = str(self.artwork.id)

        self.assertIn(key, bag)
        self.assertIn("A4", bag[key]["sizes"])

    def test_remove_from_bag(self):
        """Simple test: removing an item deletes it from session."""
        session = self.client.session
        session["bag"] = {
            str(self.artwork.id): {"sizes": {"A4": 1}}
        }
        session.save()

        self.client.post(
            self.remove_url,
            {"product_size": "A4", "next": self.view_bag_url}
        )

        bag = self.client.session.get
