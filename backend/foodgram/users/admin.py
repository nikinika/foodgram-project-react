from django.contrib import admin

from .models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    """Создание модели Юзер Администратора для админа."""

    list_display = ("pk", "username", "email", "first_name", "last_name", "password")
    search_fields = ("username", "email")
    list_filter = ("username", "email")
    empty_value_display = "-empty-"
    list_editable = ("password",)


class SubscribeAdmin(admin.ModelAdmin):
    """Создание модели Подписка Администратора для админа"""

    list_display = ("pk", "user", "author")
    list_editable = ("user", "author")
    search_fields = ("user", "author")
    list_filter = ("user", "author")
    empty_value_display = "-empty-"


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
