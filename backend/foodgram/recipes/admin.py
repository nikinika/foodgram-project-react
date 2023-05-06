from django.contrib import admin

from .models import (Favorite, Ingredient, IngredRecipe, Recipe, ShoppingList,
                     Tag)


class RecipeAdmin(admin.ModelAdmin):
    """Создание модели Рецепт Администратора для админа."""

    list_display = ("pk", "name", "author", "fav_count")
    readonly_fields = ("fav_count",)
    list_filter = (
        "author",
        "name",
        "tags",
    )
    list_editable = ("name", "author")
    empty_value_display = "-empty-"

    def fav_count(self, obj):
        return obj.recipe_fav.count()

    fav_count.short_description = "Добавлений в избранное"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
    list_editable = ("name", "measurement_unit")
    empty_value_display = "-empty-"


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    list_editable = ("name", "color", "slug")
    list_filter = ("name",)
    search_fields = ("name",)
    empty_value_display = "-empty-"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    list_editable = ("user", "recipe")


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    list_editable = ("user", "recipe")


class IngredRecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "ingredient", "amount")
    list_editable = ("recipe", "ingredient", "amount")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(IngredRecipe, IngredRecipeAdmin)
