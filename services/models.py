from django.db import models
from django.contrib.auth.models import User


class ServiceCategory(models.Model):
    """تصنيفات الخدمات"""
    name    = models.CharField(max_length=100, verbose_name="اسم التصنيف")
    icon    = models.CharField(max_length=50, blank=True, verbose_name="أيقونة Font Awesome")

    class Meta:
        verbose_name = "تصنيف خدمة"
        verbose_name_plural = "تصنيفات الخدمات"

    def __str__(self):
        return self.name


class Service(models.Model):
    """الخدمة — مقاول أو شركة تشطيب"""

    STATUS_CHOICES = [
        ('active',  'نشط'),
        ('pending', 'قيد المراجعة'),
        ('inactive','غير نشط'),
    ]

    # المعلومات الأساسية
    owner           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    category        = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, verbose_name="التصنيف")
    name            = models.CharField(max_length=200, verbose_name="اسم الشركة / المقاول")
    description     = models.TextField(verbose_name="وصف الخدمة")
    city            = models.CharField(max_length=100, verbose_name="المدينة")
    address         = models.CharField(max_length=255, blank=True, verbose_name="العنوان")
    phone           = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    whatsapp        = models.CharField(max_length=20, blank=True, verbose_name="واتساب")
    email           = models.EmailField(blank=True, verbose_name="البريد الإلكتروني")

    # التفاصيل
    min_price       = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="أقل سعر")
    max_price       = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="أعلى سعر")
    experience_years= models.PositiveIntegerField(default=0, verbose_name="سنوات الخبرة")
    is_featured     = models.BooleanField(default=False, verbose_name="مميز")
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # التقييم
    rating          = models.FloatField(default=0.0, verbose_name="التقييم")
    reviews_count   = models.PositiveIntegerField(default=0, verbose_name="عدد التقييمات")

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "خدمة"
        verbose_name_plural = "خدمات"
        ordering = ['-is_featured', '-rating', '-created_at']

    def __str__(self):
        return self.name


class ServiceImage(models.Model):
    """صور أعمال الخدمة"""
    service     = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image       = models.ImageField(upload_to='services/', verbose_name="صورة")
    is_main     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "صورة خدمة"
        verbose_name_plural = "صور الخدمات"

    def __str__(self):
        return f"صورة - {self.service.name}"


class ServiceReview(models.Model):
    """تقييمات الخدمات"""
    service     = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    rating      = models.PositiveIntegerField(default=5)
    comment     = models.TextField(verbose_name="التعليق")
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تقييم"
        verbose_name_plural = "تقييمات"
        unique_together = ['service', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"