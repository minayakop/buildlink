from django.contrib import admin
from .models import ServiceCategory, Service, ServiceImage, ServiceReview


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 3


class ServiceReviewInline(admin.TabularInline):
    model = ServiceReview
    extra = 0


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'city', 'rating', 'is_featured', 'status']
    list_filter   = ['status', 'is_featured', 'category']
    list_editable = ['is_featured', 'status']
    search_fields = ['name', 'description']
    inlines       = [ServiceImageInline, ServiceReviewInline]