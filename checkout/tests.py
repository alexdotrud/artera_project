from django.test import TestCase
from django.urls import reverse

from .models import Order


class CheckoutBasicTests(TestCase):
    def test_checkout_redirects_when_bag_empty(self):
        """
        If the bag is empty, the checkout view should redirect
        the user back to the all_artworks page.
        """
        url = reverse("checkout")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("all_artworks"))

    def test_checkout_success_renders_template(self):
        """
        checkout_success should return 200 and render the correct template
        for a valid order_number.
        """
        order = Order.objects.create(
            full_name="Test User",
            email="test@example.com",
            phone_number="123456789",
            country="SE",
            postcode="12345",
            town_or_city="Test City",
            street_address1="Test Street 1",
            street_address2="",
            county="",
            order_total=0,
            grand_total=0,
        )

        url = reverse("checkout_success", args=[order.order_number])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout_success.html")
        self.assertContains(response, order.order_number)
