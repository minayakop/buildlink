from django.db import models
from django.contrib.auth.models import User


class PropertyType(models.Model):
    """نوع العقار - شقة / فيلا / أرض / محل"""
    name = models.CharField(max_length=100, verbose_name="نوع العقار")

    class Meta:
        verbose_name = "نوع العقار"
        verbose_name_plural = "أنواع العقارات"

    def __str__(self):
        return self.name


class City(models.Model):
    """المدينة"""
    name = models.CharField(max_length=100, verbose_name="المدينة")

    class Meta:
        verbose_name = "مدينة"
        verbose_name_plural = "مدن"

    def __str__(self):
        return self.name


class District(models.Model):
    """الحي / المنطقة"""
    name = models.CharField(max_length=100, verbose_name="الحي")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts', verbose_name="المدينة")

    class Meta:
        verbose_name = "حي"
        verbose_name_plural = "أحياء"

    def __str__(self):
        return f"{self.name} - {self.city.name}"


class Property(models.Model):
    """العقار الرئيسي"""

    LISTING_TYPE_CHOICES = [
        ('sale', 'للبيع'),
        ('rent', 'للإيجار'),
    ]

    STATUS_CHOICES = [
        ('available', 'متاح'),
        ('sold', 'تم البيع'),
        ('rented', 'مؤجر'),
        ('pending', 'قيد المراجعة'),
    ]

    FINISHING_CHOICES = [
        ('furnished', 'مفروش'),
        ('semi_furnished', 'نص تشطيب'),
        ('unfurnished', 'بدون تشطيب'),
        ('core_shell', 'كور وشيل'),
    ]

    # المعلومات الأساسية
    title           = models.CharField(max_length=255, verbose_name="عنوان الإعلان")
    description     = models.TextField(verbose_name="الوصف")
    listing_type    = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, verbose_name="نوع الإعلان")
    property_type   = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, verbose_name="نوع العقار")
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available', verbose_name="الحالة")

    # الموقع
    city            = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="المدينة")
    district        = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الحي")
    address         = models.CharField(max_length=255, blank=True, verbose_name="العنوان التفصيلي")
    latitude        = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="خط العرض")
    longitude       = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="خط الطول")

    # التفاصيل
    price           = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="السعر")
    area            = models.FloatField(verbose_name="المساحة (م²)")
    bedrooms        = models.PositiveIntegerField(default=0, verbose_name="غرف النوم")
    bathrooms       = models.PositiveIntegerField(default=0, verbose_name="الحمامات")
    floor           = models.IntegerField(null=True, blank=True, verbose_name="الدور")
    finishing       = models.CharField(max_length=20, choices=FINISHING_CHOICES, blank=True, verbose_name="التشطيب")

    # المميزات
    has_garage      = models.BooleanField(default=False, verbose_name="جراج")
    has_garden      = models.BooleanField(default=False, verbose_name="حديقة")
    has_pool        = models.BooleanField(default=False, verbose_name="حمام سباحة")
    has_elevator    = models.BooleanField(default=False, verbose_name="أسانسير")
    has_security    = models.BooleanField(default=False, verbose_name="أمن وحراسة")

    # المالك والتوقيت
    owner           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', verbose_name="المالك")
    is_featured     = models.BooleanField(default=False, verbose_name="إعلان مميز")
    views_count     = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")
    avg_rating      = models.FloatField(default=0.0, verbose_name="متوسط التقييم")
    reviews_count   = models.PositiveIntegerField(default=0, verbose_name="عدد التقييمات")
    created_at      = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    updated_at      = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    class Meta:
        verbose_name = "عقار"
        verbose_name_plural = "عقارات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    """صور العقار"""
    property    = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', verbose_name="العقار")
    image       = models.ImageField(upload_to='properties/', verbose_name="الصورة")
    is_main     = models.BooleanField(default=False, verbose_name="صورة رئيسية")
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "صورة عقار"
        verbose_name_plural = "صور العقارات"

    def __str__(self):
        return f"صورة - {self.property.title}"


class PropertyReview(models.Model):
    """تقييمات العقارات"""

    RATING_CHOICES = [
        (1, '⭐ ضعيف'),
        (2, '⭐⭐ مقبول'),
        (3, '⭐⭐⭐ جيد'),
        (4, '⭐⭐⭐⭐ جيد جداً'),
        (5, '⭐⭐⭐⭐⭐ ممتاز'),
    ]

    property    = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    rating      = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)
    comment     = models.TextField(verbose_name="التعليق")
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تقييم عقار"
        verbose_name_plural = "تقييمات العقارات"
        unique_together = ['property', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"