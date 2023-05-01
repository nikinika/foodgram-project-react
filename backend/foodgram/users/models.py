from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, verbose_name="Username", unique=True)

    email = models.EmailField(verbose_name="email", unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ["id"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username}, {self.email}"


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriber")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribed"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "author"], name="Неравные значения")
        ]
