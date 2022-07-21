from django.contrib import admin

from .models import User, UserCommunity


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserCommunity)
class UserCommunityAdmin(admin.ModelAdmin):
    pass
