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

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display  = ['title', 'listing_type', 'property_type', 'city', 'price', 'status', 'is_featured', 'created_at']
    list_filter   = ['listing_type', 'status', 'is_featured', 'city', 'property_type']
    search_fields = ['title', 'description', 'address']
    list_editable = ['status', 'is_featured']
    inlines       = [PropertyImageInline, PropertyReviewInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # لما الإعلان يتوافق عليه
        if obj.status == 'available' and change:
            from django.core.mail import send_mail
            try:
                send_mail(
                    subject='تم قبول إعلانك على BuildLink! 🎉',
                    message=f'أهلاً {obj.owner.username}،\n\nتم قبول إعلانك "{obj.title}" وظهر على الموقع.\n\nشكراً لاستخدام BuildLink!',
                    from_email='noreply@buildlink.com',
                    recipient_list=[obj.owner.email],
                    fail_silently=True,
                )
            except:
                pass