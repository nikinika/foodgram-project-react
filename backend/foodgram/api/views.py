from .permissions import AuthorOrReadOnly
from .serializers import (UserSerializer, RegistrationSerializer,
                          PasswordSetSerializer, TagSerializer,
                          IngredientSerializer, CreateEditRecipeSerializer,
                          ReadRecipeSerializer, ShoppingListSerializer,
                          FavoriteSerializer, SubscribeSerializer)
from recipes.models import ShoppingList, Favorite
from users.models import User, Subscribe
from recipes.models import Tag, Ingredient, Recipe
from djoser.views import UserViewSet
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from .filters import IngredientFilter, RecipeFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.http import HttpResponse


class UserView(UserViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        if self.action == 'set_password':
            return PasswordSetSerializer
        return RegistrationSerializer

    @action(
        detail=False,
        methods=('get',),
        url_path='subscriptions',
        permission_classes=(permissions.IsAuthenticated,))
    def subscribe_list(self, request):
        queryset = Subscribe.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(page,
                                         many=True,
                                         context={'request': request})

        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly, IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return CreateEditRecipeSerializer
        return ReadRecipeSerializer

    @action(
        detail=False,
        methods=('get',),
        url_path='download_shopping_cart',
        pagination_class=None)
    def download_file(self, request):
        user = request.user
        if ShoppingList.objects.filter(user=user).exists():
            user = ShoppingList.objects.filter(user=user)
            shopping_list = 'Список покупок:\n\n'
            ingred_name = 'recipe__recipe__ingredient__name'
            measurement_unit = 'recipe__recipe__ingredient__measurement_unit'
            amount = 'recipe__recipe__amount'
            amount_sum = 'recipe__recipe__amount__sum'
            cart = user.values(
                ingred_name,
                measurement_unit).annotate(Sum(amount)).order_by(ingred_name)
            for _ in cart:
                shopping_list += (
                    f'{_[ingred_name]} ({_[measurement_unit]})'
                    f' — {_[amount_sum]}\n'
                )
            file = HttpResponse(shopping_list, content_type='text/plain')
            filename = 'c'
            file['Content-Disposition'] = (
                f'attachment; filename={filename}'
                )
            return file
        return Response('No recipes in Shopping Lists',
                        status=status.HTTP_400_BAD_REQUEST)


class ShoppingListViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = ShoppingListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user.id
        return ShoppingList.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(Recipe,
                                     id=self.kwargs.get('recipe_id')))

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        user = request.user
        if ShoppingList.objects.filter(recipe_id=recipe_id,
                                       user=user).exists():
            get_object_or_404(ShoppingList,
                              user=user,
                              recipe=recipe_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Recipe not in Shopping List'},
                        status=status.HTTP_400_BAD_REQUEST)


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user.id
        return Favorite.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(Recipe,
                                     id=self.kwargs.get('recipe_id')))

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        user = request.user
        if Favorite.objects.filter(recipe_id=recipe_id,
                                   user=user).exists():
            get_object_or_404(Favorite,
                              user=user,
                              recipe_id=recipe_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Recipe not in Favorite'},
                        status=status.HTTP_400_BAD_REQUEST)


class SubscribeViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return self.request.user.subscriber.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['author_id'] = self.kwargs.get('user_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            author=get_object_or_404(
                User,
                id=self.kwargs.get('user_id')))

    @action(methods=('delete',), detail=True)
    def delete(self, request, user_id):
        get_object_or_404(User, id=user_id)
        if Subscribe.objects.filter(user=request.user,
                                    author_id=user_id).exists():
            get_object_or_404(Subscribe,
                              user=request.user,
                              author_id=user_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Subscribe wasn`t create'},
                        status=status.HTTP_400_BAD_REQUEST)
