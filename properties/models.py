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
    title = models.CharField(max_length=255, verbose_name="عنوان الإعلان")
    description = models.TextField(verbose_name="الوصف")
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, db_index=True, verbose_name="نوع الإعلان")
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, verbose_name="نوع العقار")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available', db_index=True, verbose_name="الحالة")

    # الموقع
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="المدينة")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الحي")
    address = models.CharField(max_length=255, blank=True, verbose_name="العنوان التفصيلي")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="خط العرض")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="خط الطول")

    # التفاصيل
    price = models.DecimalField(max_digits=12, decimal_places=2, db_index=True, verbose_name="السعر")
    area = models.FloatField(verbose_name="المساحة (م²)")
    bedrooms = models.PositiveIntegerField(default=0, verbose_name="غرف النوم")
    bathrooms = models.PositiveIntegerField(default=0, verbose_name="الحمامات")
    floor = models.IntegerField(null=True, blank=True, verbose_name="الدور")
    finishing = models.CharField(max_length=20, choices=FINISHING_CHOICES, blank=True, verbose_name="التشطيب")

    # المميزات
    has_garage = models.BooleanField(default=False, verbose_name="جراج")
    has_garden = models.BooleanField(default=False, verbose_name="حديقة")
    has_pool = models.BooleanField(default=False, verbose_name="حمام سباحة")
    has_elevator = models.BooleanField(default=False, verbose_name="أسانسير")
    has_security = models.BooleanField(default=False, verbose_name="أمن وحراسة")

    # بيانات التواصل
    phone = models.CharField(max_length=20, blank=True, verbose_name="رقم الهاتف")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="واتساب")

    # المالك والتوقيت
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', verbose_name="المالك")
    is_featured = models.BooleanField(default=False, db_index=True, verbose_name="إعلان مميز")
    views_count = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")
    avg_rating = models.FloatField(default=0.0, verbose_name="متوسط التقييم")
    reviews_count = models.PositiveIntegerField(default=0, verbose_name="عدد التقييمات")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="تاريخ الإضافة")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    class Meta:
        verbose_name = "عقار"
        verbose_name_plural = "عقارات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_main_image(self):
        """إرجاع الصورة الرئيسية أو الأولى أو صورة افتراضية"""
        main_img = self.images.filter(is_main=True).first()
        if not main_img:
            main_img = self.images.first()
        return main_img.image.url if main_img else '/static/images/property-placeholder.jpg'

    def get_whatsapp_link(self):
        """توليد رابط مباشر لمحادثة الواتساب"""
        number = self.whatsapp or self.phone
        if number:
            clean_number = ''.join(filter(str.isdigit, str(number)))
            if clean_number.startswith('01'):
                clean_number = '2' + clean_number
            return f"https://wa.me/{clean_number}?text=مرحباً،%20أنا%20مهتم%20بالعقار:%20{self.title}"
        return "#"


class PropertyImage(models.Model):
    """صور العقار"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', verbose_name="العقار")
    image = models.ImageField(upload_to='properties/', verbose_name="الصورة")
    is_main = models.BooleanField(default=False, verbose_name="صورة رئيسية")
    created_at = models.DateTimeField(auto_now_add=True)

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

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews', verbose_name="العقار")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5, verbose_name="التقييم")
    comment = models.TextField(verbose_name="التعليق")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التقييم")

    class Meta:
        verbose_name = "تقييم عقار"
        verbose_name_plural = "تقييمات العقارات"
        unique_together = ['property', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"