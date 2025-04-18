"""
Tests for the ingredients APIs.
"""
# from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Ingredient,
    # Recipe
)

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """create and return an ingredient url."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='user@example.com', password='testpass123'):
    """create and return a new user with given defaults."""
    return get_user_model().objects.create_user(
        email=email,
        password=password,
    )


class PublicIngredientsAPITest(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrievin ingredients."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients."""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Vanilla')

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user"""
        user2 = create_user(email='user2new@example.com')
        Ingredient.objects.create(user=user2, name='Salt')
        ingredient = Ingredient.objects.create(user=self.user, name='Pepper')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating an ingredient"""
        ing = Ingredient.objects.create(user=self.user, name='cilantro')

        payload = {
            'name': 'Carrot',
        }
        url = detail_url(ing.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ing.refresh_from_db()
        self.assertEqual(ing.name, payload['name'])

    def test_delete_ingredient(self):
        """Test Deleting an ingredient."""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='lettuce'
        )

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())

    # def test_filter_ingredients_assigned_to_recipes(self):
    #     """Test listing ingrefients to those assigned to recipes."""
    #     in1 = Ingredient.objects.create(user=self.user, name="apple")
    #     in2 = Ingredient.objects.create(user=self.user, name="orange")
    #     recipe = Recipe.objects.create(
    #         title='salad',
    #         time_minutes=5,
    #         price=Decimal('4.50'),
    #         user=self.user
    #     )
    #     recipe.ingredients.add(in1)

    #     res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

    #     s1 = IngredientSerializer(in1)
    #     s2 = IngredientSerializer(in2)
    #     self.assertIn(s1.data, res.data)
    #     self.assertNotIn(s2.data, res.data)

    # def test_filter_ingredients_unique(self):
    #     """Test filter ingredients returns a unique list."""
    #     ing = Ingredient.objects.create(user=self.user, name='eggs')
    #     Ingredient.objects.create(user=self.user, name='carrot')
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
    #     r1.ingredients.add(ing)
    #     r2.ingredients.add(ing)

    #     res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

    #     self.assertEqual(len(res.data), 1)
