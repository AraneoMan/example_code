from django.contrib import admin

from .models import Creation, CreationType, CreationFile


@admin.register(Creation)
class CreationAdmin(admin.ModelAdmin):
    pass


@admin.register(CreationType)
class CreationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CreationFile)
class CreationFileAdmin(admin.ModelAdmin):
    pass
