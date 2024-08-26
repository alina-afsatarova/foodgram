from django.db.models import Count, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (
    Favorite, Ingredient, IngredientRecipe,
    Recipe, ShoppingCart, Tag
)
from users.models import Subscription, User
from .filters import RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CustomUserSerializer, IngredientSerializer,
    RecipeCreateSerializer, RecipeReadSerializer,
    ShortRecipeSerializer, SubscriptionSerializer,
    TagSerializer
)
from .utils import get_short_link


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=['get', ],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['put', ],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def avatar(self, request, **kwargs):
        avatar = request.data.get('avatar')
        if not avatar:
            raise serializers.ValidationError(
                'Аватар не добавлен!'
            )
        serializer = CustomUserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'avatar': serializer.data.get('avatar')},
            status=status.HTTP_200_OK
        )

    @avatar.mapping.delete
    def delete_avatar(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        user.avatar = ''
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get', ],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscriptions(self, request):
        subscribed_to = User.objects.filter(
            subscription__user=request.user
        ).annotate(recipes_count=Count('recipes'))
        page = self.paginate_queryset(subscribed_to)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    def get_subscribed_to(self, id):
        return get_object_or_404(
            User.objects.annotate(recipes_count=Count('recipes')),
            id=id
        )

    @action(
        detail=True,
        methods=['post', ],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, id):
        subscribed_to = self.get_subscribed_to(id=id)
        serializer = SubscriptionSerializer(
            subscribed_to,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Subscription.objects.create(
            user=request.user, subscribed_to=subscribed_to
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        try:
            subscription = Subscription.objects.get(
                user=request.user, subscribed_to=self.get_subscribed_to(id=id)
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            short_link=get_short_link(Recipe)
        )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=['get', ],
        permission_classes=(permissions.AllowAny,),
        url_path='get-link'
    )
    def get_link(self, request, **kwargs):
        recipe = Recipe.objects.get(id=kwargs['pk'])
        return Response(
            {'short-link':
             request.build_absolute_uri('/') + 's/' + recipe.short_link},
            status=status.HTTP_200_OK
        )

    def get_recipe(self, id):
        return get_object_or_404(Recipe, id=id)

    def post_func(self, request, id, model):
        recipe = self.get_recipe(id=id)
        serializer = ShortRecipeSerializer(
            recipe,
            data=request.data,
            context={'request': request, 'model': model}
        )
        serializer.is_valid(raise_exception=True)
        model.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_func(self, request, id, model):
        try:
            obj = model.objects.get(
                user=request.user,
                recipe=self.get_recipe(id=id)
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', ],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, **kwargs):
        return self.post_func(request=request, id=kwargs['pk'], model=Favorite)

    @favorite.mapping.delete
    def delete_favorite(self, request, **kwargs):
        return self.delete_func(
            request=request, id=kwargs['pk'], model=Favorite
        )

    @action(
        detail=True,
        methods=['post', ],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, **kwargs):
        return self.post_func(
            request=request, id=kwargs['pk'], model=ShoppingCart
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, **kwargs):
        return self.delete_func(
            request=request, id=kwargs['pk'], model=ShoppingCart
        )

    @action(
        detail=False,
        methods=['get', ],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request, **kwargs):
        indredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ). values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount_sum=Sum('amount'))
        shopping_cart = ''
        for ingredient in indredients:
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['amount_sum']
            shopping_cart += f'{name} ({measurement_unit}) - {amount}\n'
        return HttpResponse(shopping_cart, content_type='text/plain')
