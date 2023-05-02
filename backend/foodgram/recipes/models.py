from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование")

    measurement_unit = models.CharField(
        max_length=200, verbose_name="Единица измерения"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name="Цвет в HEX",
        validators=[RegexValidator(r"^#([a-fA-F0-9]{6})")],
    )

    slug = models.SlugField(
        max_length=200,
        null=True,
        unique=True,
        verbose_name="Уникальный слаг",
        validators=[RegexValidator(r"^[-a-zA-Z0-9_]+$")],
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes", verbose_name="Автор"
    )

    name = models.CharField(max_length=200, verbose_name="Название")

    image = models.ImageField(
        verbose_name="Изображение", upload_to="recipes/images/", blank=True
    )

    text = models.TextField(verbose_name="Описание")

    tags = models.ManyToManyField(Tag, verbose_name="Тег")

    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления, мин", validators=[MinValueValidator(1)]
    )

    ingredients = models.ManyToManyField(
        Ingredient, through="IngredRecipe", verbose_name="Ингридиенты"
    )

    pub_date = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class IngredRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт", related_name="recipe"
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиенты",
        related_name="ingredient",
    )

    amount = models.PositiveIntegerField(
        verbose_name="Количество", validators=[MinValueValidator(0)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"], name="Неравные ингридиенты"
            )
        ]

    def __str__(self):
        return f"{self.recipe}, {self.ingredient}, {self.amount}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user_fav",
        on_delete=models.CASCADE,
        verbose_name="Добавлено в избранное",
    )

    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_fav",
        on_delete=models.CASCADE,
        verbose_name="Рецепт в избранном",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="Неравные избранные"
            )
        ]

    def __str__(self):
        return f"{self.user.username}, {self.recipe.name}"


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user_basket",
        on_delete=models.CASCADE,
        verbose_name="Добавлено в корзину",
    )

    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_basket",
        on_delete=models.CASCADE,
        verbose_name="Рецепт в корзине",
    )

    def __str__(self):
        return f"{self.user.username}, {self.recipe.name}"
