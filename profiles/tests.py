from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from checkout.models import Order, OrderItem
from services.models import ArtworkRequest
from shop.models import Artwork, Category

User = get_user_model()


class ProfileViewTests(TestCase):
    """Basic tests for the profile and library views."""

    def setUp(self):
        self.profile_url = reverse("profile")
        self.library_url = reverse("library")
        self.login_url = reverse("account_login")

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
        )

    def test_profile_redirects_if_not_logged_in(self):
        """Profile view should redirect anonymous users to login."""
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)

    def test_profile_renders_for_logged_in_user(self):
        """Profile view should return 200 for logged-in users."""
        self.client.login(username="testuser", password="testpassword123")

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")

    def test_library_redirects_if_not_logged_in(self):
        """Library view should redirect anonymous users to login."""
        response = self.client.get(self.library_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)

    def test_library_renders_for_logged_in_user(self):
        """Library view should return 200 for logged-in users."""
        self.client.login(username="testuser", password="testpassword123")

        response = self.client.get(self.library_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/library.html")

    def test_library_displays_orders_and_requests(self):
        """
        Library should show the user's orders and artwork requests.
        """
        # Log in first (library is login_required)
        self.client.login(username="testuser", password="testpassword123")

        category = Category.objects.create(name="TestCategory")
        artwork = Artwork.objects.create(
            name="Test Artwork",
            description="Test description",
            price=Decimal("10.00"),
            category=category,
        )
        order = Order.objects.create(
            user=self.user,
            full_name="Test User",
            email=self.user.email,
            phone_number="123456789",
            country="SE",
            postcode="12345",
            town_or_city="Test City",
            street_address1="Street 1",
            street_address2="",
            county="",
            order_total=Decimal("10.00"),
            grand_total=Decimal("10.00"),
        )

        OrderItem.objects.create(
            order=order,
            artwork=artwork,
            quantity=1,
            size="S",
        )

        ArtworkRequest.objects.create(
            user=self.user,
            title="Custom Request",
            description="Test request",
            status="in_review",
        )

        response = self.client.get(self.library_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.order_number)
        self.assertContains(response, "Test Artwork")
        self.assertContains(response, "Custom Request")
