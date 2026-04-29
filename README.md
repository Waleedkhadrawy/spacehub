# SpaceHub — منصة تأجير المساحات 🏢

منصة ويب متكاملة لتأجير المساحات في المملكة العربية السعودية (مكاتب، قاعات، استوديوهات، مستودعات، مساحات فعاليات).

## المفاهيم المُطبَّقة

| المفهوم | التطبيق |
|---|---|
| Authentication | تسجيل دخول / خروج، `login_required` |
| Authorization | Groups (Owner / Tenant)، `has_perm` |
| ORM Relationships | ForeignKey، OneToOneField، `related_name` |
| Q Objects | البحث عبر title, description, address |
| F Objects | مقارنة حقول DB في استعلامات الحجز |
| Aggregate / Annotate | متوسط التقييمات، عدد الحجوزات |
| Field Choices | TextChoices لـ SpaceType، City، BookingStatus |
| Transactions | `transaction.atomic()` عند إنشاء الحجز |
| Pagination | `Paginator` على قائمة المساحات (9 لكل صفحة) |
| Messages | Flash messages (success, error, warning, info) |
| Media Files | `ImageField`، Cloudinary / local storage |
| Django Admin | `list_display`، `list_filter`، Inline |
| Signals | `post_save` لإنشاء UserProfile تلقائياً |

## البنية

```
spacehub/
├── accounts/      # تسجيل، دخول، ملف شخصي، لوحة تحكم
├── spaces/        # إدارة المساحات + بحث + pagination
├── bookings/      # الحجز مع transaction.atomic
├── reviews/       # التقييمات مع unique_together
├── templates/     # قوالب Bootstrap RTL
└── spacehub/      # إعدادات المشروع
```

## التشغيل المحلي

```bash
git clone https://github.com/Waleedkhadrawy/spacehub.git
cd spacehub
pip install -r requirements.txt
cp .env.example .env   # أضف قيمك الخاصة
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## المتطلبات

- Python 3.10+
- Django 5.x
- Pillow
- python-dotenv
- cloudinary / django-cloudinary-storage
