from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import Favorite, Ingredient, IngredRecipe, Recipe, ShoppingList, Tag
from users.models import Subscribe, User
from django.contrib.auth.hashers import check_password


class UserReadSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and not request.user.is_anonymous:
            return Subscribe.objects.filter(user=request.user, author=obj).exists()
        return False


class RegistrationSerializer(UserCreateSerializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )
    email = serializers.EmailField(max_length=254, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password")

    def validate(self, data):
        if data.get("username").lower() == "me":
            raise ValidationError('"me" is not valid username')
        if User.objects.filter(email=data.get("email")).exists():
            user = User.objects.get(email=data.get("email"))
            if user.username != data.get("username"):
                raise ValidationError("invalid email")
        if User.objects.filter(username=data.get("username")).exists():
            user = User.objects.get(username=data.get("username"))
            if user.email != data.get("email"):
                raise ValidationError("invalid username")
        return data


class PasswordSetSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, label="Текущий пароль")
    new_password = serializers.CharField(required=True, label="Новый пароль")

    def update(self, instance, validated_data):
        if validated_data["current_password"] == validated_data["new_password"]:
            raise serializers.ValidationError(
                {"new_password": "Equal passwords"}
            )
        instance.set_password(validated_data["new_password"])
        if not instance.check_password(validated_data["current_password"]):
            raise serializers.ValidationError(
                {"current_password": "Wrong current password."}
            )
        instance.save()
        return validated_data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class EngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source="ingredient.id",
    )
    name = serializers.ReadOnlyField(
        source="ingredient.name",
    )
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit",
    )

    class Meta:
        model = IngredRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserReadSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = EngredientAmountSerializer(many=True, source="recipe")
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        return (
            request.user.is_authenticated
            and Favorite.objects.filter(user=request.user, recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        return (
            request.user.is_authenticated
            and ShoppingList.objects.filter(user=request.user, recipe=obj).exists()
        )


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredRecipe
        fields = (
            "id",
            "amount",
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = AddIngredientSerializer(many=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "author",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredRecipe.objects.bulk_create(
                [
                    IngredRecipe(
                        recipe=recipe,
                        ingredient_id=ingredient.get("id"),
                        amount=ingredient.get("amount"),
                    )
                ]
            )

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(
            author=self.context["request"].user, **validated_data
        )
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if "tags" in validated_data:
            instance.tags.set(validated_data.pop("tags"))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class ShoppingListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="recipe.id")
    name = serializers.ReadOnlyField(source="recipe.name")
    image = serializers.ImageField(source="recipe.image", read_only=True)
    cooking_time = serializers.ReadOnlyField(source="recipe.cooking_time")

    class Meta:
        model = ShoppingList
        fields = ("id", "name", "image", "cooking_time")


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source="recipe.id",
    )
    name = serializers.ReadOnlyField(
        source="recipe.name",
    )
    image = Base64ImageField(
        source="recipe.image",
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source="recipe.cooking_time",
    )

    class Meta:
        model = Favorite
        fields = ("id", "name", "image", "cooking_time")

    def validate(self, data):
        user = self.context.get("request").user
        recipe = self.context.get("recipe_id")
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError({"errors": "Recipe already in Favorite"})
        return data


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="author.email", read_only=True)
    id = serializers.IntegerField(source="author.pk", read_only=True)
    username = serializers.CharField(source="author.username", read_only=True)
    first_name = serializers.CharField(source="author.first_name", read_only=True)
    last_name = serializers.CharField(source="author.last_name", read_only=True)
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def validate(self, data):
        user_id = self.context.get("request").user.pk
        author_id = int(self.context.get("author_id"))
        if user_id == author_id:
            raise serializers.ValidationError({"errors": "Denied"})
        if Subscribe.objects.filter(user_id=user_id, author_id=author_id).exists():
            raise serializers.ValidationError({"errors": "You`ve already Subscribed"})
        return data

    def get_recipes(self, obj):
        recipes = obj.author.recipes.all()
        return SubscribeRecipeSerializer(recipes, many=True).data

    def get_is_subscribed(self, obj):
        if Subscribe.objects.filter(
            user=self.context.get("request").user, author=obj.author
        ).exists():
            return True
        return False

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()
