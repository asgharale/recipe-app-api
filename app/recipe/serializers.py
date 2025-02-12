"""
Serializers for Recipe APIs.
"""
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """serializer for recipes."""

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id']
