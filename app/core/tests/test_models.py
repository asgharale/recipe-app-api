"""
Test for models
"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


def create_user(email='user@example.com', password='testpass123'):
    """create and return a new user with given defaults."""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


class ModelTest(TestCase):
    """Test models"""
    def test_create_user_with_email_success(self):
        """Test Creating an user with email successfully."""
        email = "test@example.com"
        password = 'samplepass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_emailnormalized(self):
        """testing new user's email is normalized."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='samplepass123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        """Creating user without an email raises an error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "samplepass123")

    def tet_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            email="test@example.com",
            password='samplepass123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating recipe successfully."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='sample recipe description',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(
            user=user,
            name='Tag1'
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """test creating a ingredient successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient 1'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuif(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f"uploads/recipe/{uuid}.jpg")
