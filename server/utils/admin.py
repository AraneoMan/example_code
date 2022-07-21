from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
