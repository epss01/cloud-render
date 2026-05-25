from django.contrib import admin
from .models import Album, Photo


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'photo_count', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'album', 'uploaded_by')
    search_fields = ('title', 'description')
    readonly_fields = ('uploaded_at',)