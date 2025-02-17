"""
URL mapping for recipe app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewset)
router.register('tags', views.TagViewset)
router.register('ingredients', views.IngredientViewset)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
