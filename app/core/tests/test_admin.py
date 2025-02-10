"""
Tests for django admin modification.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class AdminSiteTests(TestCase):
    """Tests for django admin."""

    def setUp(self):
        """Creating Client and User."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='sampleadmin@example.com',
            password='samplepass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='sampleuser@example.com',
            password='samplepass123',
            name="Test User"
        )

    def test_users_list(self):
        """Test that users are listed on page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
