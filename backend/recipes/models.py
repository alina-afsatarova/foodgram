from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=(RegexValidator(r'^[\w.@+-]+\Z'),),
    )
    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    #avatar = models.ImageField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Ingredient(models.Model):
    name = models.CharField(max_length=128, blank=False)
    measurement_unit = models.CharField(max_length=64, blank=False)


class Tag(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(
        max_length=32,
        unique=True,
        validators=(RegexValidator(r'^[-a-zA-Z0-9_]+$'),),
    )


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False)
    #image = models.ImageField(blank=False)
    text = models.TextField(blank=False)
    ingredients = models.ManyToManyField(Ingredient, blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    cooking_time = models.IntegerField(blank=False)


class ShoppingCart(models.Model):
    pass


class Favorite(models.Model):
    pass


class Subscription(models.Model):
    pass
