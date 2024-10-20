from django.contrib import admin
from pages.models import *


@admin.register(GalleryImageCategory)
class GalleryImageCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date')
    search_fields = ('name',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'created_at')
    search_fields = ('image',)
