from django.contrib import admin
from .models import Property, PropertyImage, PropertyType, City, District, PropertyReview


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


class PropertyReviewInline(admin.TabularInline):
    model = PropertyReview
    extra = 0
    readonly_fields = ['user', 'rating', 'comment', 'created_at']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display  = ['title', 'listing_type', 'property_type', 'city', 'price', 'status', 'is_featured', 'created_at']
    list_filter   = ['listing_type', 'status', 'is_featured', 'city', 'property_type']
    search_fields = ['title', 'description', 'address']
    list_editable = ['status', 'is_featured']
    inlines       = [PropertyImageInline, PropertyReviewInline]
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('title', 'description', 'listing_type', 'property_type', 'status', 'owner')
        }),
        ('الموقع', {
            'fields': ('city', 'district', 'address', 'latitude', 'longitude')
        }),
        ('التفاصيل', {
            'fields': ('price', 'area', 'bedrooms', 'bathrooms', 'floor', 'finishing')
        }),
        ('المميزات', {
            'fields': ('has_garage', 'has_garden', 'has_pool', 'has_elevator', 'has_security')
        }),
        ('إعدادات الإعلان', {
            'fields': ('is_featured', 'views_count')
        }),
    )


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']
    list_filter  = ['city']