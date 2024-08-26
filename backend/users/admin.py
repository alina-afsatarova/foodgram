from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin

from .models import CustomGroup, Subscription, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribed_to')
    search_fields = ('user__username', 'subscribed_to__username')


admin.site.unregister(Group)


@admin.register(CustomGroup)
class GroupAdmin(GroupAdmin):
    pass
