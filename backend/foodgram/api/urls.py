from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    FavoriteViewSet,
    IngredientViewSet,
    RecipeViewSet,
    ShoppingListViewSet,
    SubscribeViewSet,
    TagViewSet,
    UserView,
)

router = DefaultRouter()
router.register(r"users", UserView, basename="users")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"ingredients", IngredientViewSet, basename="ingredients")
router.register(r"recipes", RecipeViewSet, basename="recipes")
router.register(
    r"recipes/(?P<recipe_id>\d+)/shopping_cart",
    ShoppingListViewSet,
    basename="shopping_cart",
)
router.register(
    r"recipes/(?P<recipe_id>\d+)/favorite", FavoriteViewSet, basename="favorite"
)
router.register(
    r"users/(?P<user_id>\d+)/subscribe", SubscribeViewSet, basename="subscribe"
)

urlpatterns = [
    path("", include(router.urls)),
    path(r"auth/", include("djoser.urls.authtoken")),
    path("", include("djoser.urls")),
]
