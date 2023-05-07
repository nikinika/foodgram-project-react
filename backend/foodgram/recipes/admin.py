from django.contrib import admin

from .models import (Favorite, Ingredient, IngredRecipe, Recipe, ShoppingList,
                     Tag)


class RecipeAdmin(admin.ModelAdmin):
    """Создание модели Рецепт Администратора для админа."""

    list_display = ("pk", "name", "author", "pub_date", "tags", "fav_count")
    readonly_fields = ("fav_count",)
    list_filter = (
        "author",
        "name",
        "tags",
    )
    empty_value_display = "-empty-"

    def fav_count(self, obj):
        return obj.recipe_fav.count()

    fav_count.short_description = "Добавлений в избранное"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-empty-"


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    list_filter = ("name",)
    search_fields = ("name",)
    empty_value_display = "-empty-"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")


class IngredRecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "ingredient", "amount")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(IngredRecipe, IngredRecipeAdmin)
