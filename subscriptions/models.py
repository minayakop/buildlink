from django.db import models
from django.contrib.auth.models import User


class Plan(models.Model):
    """باقات الاشتراك"""

    PLAN_TYPE_CHOICES = [
        ('free',     'مجاني'),
        ('basic',    'أساسي'),
        ('pro',      'احترافي'),
        ('business', 'أعمال'),
    ]

    name            = models.CharField(max_length=100, verbose_name="اسم الباقة")
    plan_type       = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES, unique=True)
    price           = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    duration_days   = models.PositiveIntegerField(default=30, verbose_name="مدة الاشتراك (يوم)")
    max_listings    = models.PositiveIntegerField(default=3, verbose_name="أقصى عدد إعلانات")
    featured_count  = models.PositiveIntegerField(default=0, verbose_name="إعلانات مميزة")
    description     = models.TextField(blank=True)
    is_active       = models.BooleanField(default=True)

    class Meta:
        verbose_name = "باقة"
        verbose_name_plural = "باقات"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """اشتراك المستخدم"""

    STATUS_CHOICES = [
        ('active',   'نشط'),
        ('expired',  'منتهي'),
        ('cancelled','ملغي'),
    ]

    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan        = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date  = models.DateTimeField(auto_now_add=True)
    end_date    = models.DateTimeField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "اشتراك"
        verbose_name_plural = "اشتراكات"

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    def is_valid(self):
        from django.utils import timezone
        return self.status == 'active' and (
            self.end_date is None or self.end_date > timezone.now()
        )


class FeaturedListing(models.Model):
    """الإعلانات المميزة المدفوعة"""

    property    = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date  = models.DateTimeField(auto_now_add=True)
    end_date    = models.DateTimeField()
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    is_active   = models.BooleanField(default=True)

    class Meta:
        verbose_name = "إعلان مميز"
        verbose_name_plural = "إعلانات مميزة"

    def __str__(self):
        return f"{self.property.title} - مميز"