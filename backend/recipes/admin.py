from django.contrib import admin

from .models import (
    Favorite, Ingredient, IngredientRecipe,
    Recipe, ShoppingCart, Subscription,
    Tag, TagRecipe, User
)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites')
    search_fields = ('name', 'author',)
    list_filter = ('tags',)

    @admin.display(description='Число добавлений в избранное')
    def favorites(self, obj):
        return obj.favorite.count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribed_to')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('tag', 'recipe')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
