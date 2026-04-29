from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class SpaceType(models.TextChoices):
    OFFICE = 'office', 'مكتب'
    HALL = 'hall', 'قاعة'
    STUDIO = 'studio', 'استوديو'
    WAREHOUSE = 'warehouse', 'مستودع'
    EVENT = 'event', 'مساحة فعاليات'


class SpaceStatus(models.TextChoices):
    AVAILABLE = 'available', 'متاح'
    UNAVAILABLE = 'unavailable', 'غير متاح'


class City(models.TextChoices):
    RIYADH = 'riyadh', 'الرياض'
    JEDDAH = 'jeddah', 'جدة'
    DAMMAM = 'dammam', 'الدمام'
    MAKKAH = 'makkah', 'مكة المكرمة'
    MADINAH = 'madinah', 'المدينة المنورة'
    KHOBAR = 'khobar', 'الخبر'
    ABHA = 'abha', 'أبها'
    TABUK = 'tabuk', 'تبوك'


class Space(models.Model):
    """نموذج المساحة الرئيسي — ForeignKey مع المالك"""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='spaces',
        verbose_name='المالك'
    )
    title = models.CharField(max_length=200, verbose_name='اسم المساحة')
    description = models.TextField(verbose_name='الوصف')
    space_type = models.CharField(
        max_length=20,
        choices=SpaceType.choices,
        default=SpaceType.OFFICE,
        verbose_name='نوع المساحة'
    )
    status = models.CharField(
        max_length=20,
        choices=SpaceStatus.choices,
        default=SpaceStatus.AVAILABLE,
        verbose_name='الحالة'
    )
    city = models.CharField(
        max_length=20,
        choices=City.choices,
        default=City.RIYADH,
        verbose_name='المدينة'
    )
    address = models.CharField(max_length=300, verbose_name='العنوان')
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='السعر / اليوم (ريال)'
    )
    capacity = models.IntegerField(default=1, verbose_name='السعة (أشخاص)')
    area_sqm = models.FloatField(default=0, verbose_name='المساحة (متر مربع)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'مساحة'
        verbose_name_plural = 'المساحات'

    def __str__(self):
        return f"{self.title} — {self.get_city_display()}"

    def average_rating(self):
        result = self.reviews.aggregate(avg=Avg('rating'))
        return result['avg'] or 0

    def main_image(self):
        img = self.images.first()
        return img.image if img else None


class SpaceImage(models.Model):
    """صور المساحة — ForeignKey مع Space"""

    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='spaces/', verbose_name='صورة')
    is_main = models.BooleanField(default=False, verbose_name='صورة رئيسية')

    def __str__(self):
        return f"صورة لـ {self.space.title}"
