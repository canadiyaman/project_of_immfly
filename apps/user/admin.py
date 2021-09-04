from django.contrib import admin

from apps.user.models import User

__all__ = ['UserAdmin']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', )
