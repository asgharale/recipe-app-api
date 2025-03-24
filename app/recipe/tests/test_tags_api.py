"""
Tests for the tags API.
"""
# from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Tag,
    # Recipe
)

from recipe.serializers import (
    TagSerializer
)


TAGS_URL = reverse('recipe:tag-list')


def create_user(email='user@example.com', password='testpass123'):
    """create and return a new user with given defaults."""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


def detail_url(tag_id):
    """create and return tag detail url."""
    return reverse('recipe:tag-detail', args=[tag_id])


class PublicTagsAPITests(TestCase):
    """test unathenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """test auth is required for retireving tags."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITest(TestCase):
    """test Authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """test retrieving a list of tags."""
        Tag.objects.create(user=self.user, name='sample tag')
        Tag.objects.create(user=self.user, name='sample tag 2')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """test listed tags is limited to authenticated user."""
        new_user = create_user(email='new@example.com')
        Tag.objects.create(user=new_user, name='dessert')
        tag = Tag.objects.create(user=self.user, name='ok name')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """Test updating tag."""
        tag = Tag.objects.create(user=self.user, name='after dinner')

        payload = {'name': 'Dessert'}
        url = detail_url(tag.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(payload['name'], tag.name)

    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = Tag.objects.create(user=self.user, name='Breakfast')

        url = detail_url(tag.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

    # def test_filter_tags_assigned_to_recipes(self):
    #     """Test listing tags to those assigned to recipes."""
    #     tag1 = Tag.objects.create(user=self.user, name="apple")
    #     tag2 = Tag.objects.create(user=self.user, name="orange")
    #     recipe = Recipe.objects.create(
    #         title='salad',
    #         time_minutes=5,
    #         price=Decimal('4.50'),
    #         user=self.user
    #     )
    #     recipe.tags.add(tag1)

    #     res = self.client.get(TAGS_URL, {'assigned_only': 1})

    #     s1 = TagSerializer(tag1)
    #     s2 = TagSerializer(tag2)
    #     self.assertIn(s1.data, res.data)
    #     self.assertNotIn(s2.data, res.data)

    # def test_filter_tags_unique(self):
    #     """Test filter tags returns a unique list."""
    #     tag = Tag.objects.create(user=self.user, name='eggs')
    #     Tag.objects.create(user=self.user, name='carrot')
    #     r1 = Recipe.objects.create(
    #         title='scrambled eggs',
    #         time_minutes=5,
    #         price=Decimal('2.50'),
    #         user=self.user
    #     )
    #     r2 = Recipe.objects.create(
    #         title='herb eggs',
    #         time_minutes=15,
    #         price=Decimal('1.50'),
    #         user=self.user
    #     )
    #     r1.tags.add(tag)
    #     r2.tags.add(tag)

    #     res = self.client.get(TAGS_URL, {'assigned_only': 1})

    #     self.assertEqual(len(res.data), 1)
