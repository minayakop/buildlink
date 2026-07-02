from django.contrib import admin
from .models import Plan, Subscription, FeaturedListing


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'max_listings', 'featured_count', 'is_active']
    list_editable = ['price', 'is_active']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date']
    list_filter  = ['status', 'plan']


@admin.register(FeaturedListing)
class FeaturedListingAdmin(admin.ModelAdmin):
    list_display = ['property', 'user', 'start_date', 'end_date', 'amount_paid', 'is_active']