from django.contrib import admin
from .models import Space, SpaceImage


class SpaceImageInline(admin.TabularInline):
    model = SpaceImage
    extra = 1


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'space_type', 'city', 'status', 'price_per_day', 'created_at']
    list_filter = ['space_type', 'status', 'city']
    search_fields = ['title', 'owner__username', 'address']
    inlines = [SpaceImageInline]
    raw_id_fields = ['owner']


@admin.register(SpaceImage)
class SpaceImageAdmin(admin.ModelAdmin):
    list_display = ['space', 'is_main']
    list_filter = ['is_main']
