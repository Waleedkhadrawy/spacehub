# دليل تشغيل مشروع SpaceHub على جهاز جديد
## (التفصيل الممل الكامل)

---

## المحتويات

1. [تثبيت Python](#1-تثبيت-python)
2. [تحميل المشروع من GitHub](#2-تحميل-المشروع-من-github)
3. [إنشاء البيئة الافتراضية](#3-إنشاء-البيئة-الافتراضية-virtual-environment)
4. [تثبيت المتطلبات](#4-تثبيت-المتطلبات)
5. [إعداد ملف .env](#5-إعداد-ملف-env)
6. [تشغيل قاعدة البيانات](#6-تشغيل-قاعدة-البيانات)
7. [إنشاء حساب المدير](#7-إنشاء-حساب-المدير-superuser)
8. [تشغيل السيرفر](#8-تشغيل-السيرفر)
9. [مشاكل شائعة وحلولها](#9-مشاكل-شائعة-وحلولها)

---

## 1. تثبيت Python

### Windows
1. اذهب إلى: **https://www.python.org/downloads/**
2. حمّل أحدث إصدار من Python 3 (مثلاً Python 3.12.x)
3. افتح الملف المحمّل (`python-3.12.x-amd64.exe`)
4. **مهم جداً:** ضع علامة ✅ على **"Add Python to PATH"** قبل الضغط على Install
5. اضغط **"Install Now"**
6. بعد الانتهاء، افتح **Command Prompt** (ابحث عنه في Start Menu)
7. اكتب هذا للتأكد:
   ```
   python --version
   ```
   يجب أن يظهر: `Python 3.12.x`

### macOS
1. اذهب إلى: **https://www.python.org/downloads/**
2. حمّل Python 3.12 لـ macOS
3. افتح الملف `.pkg` واتبع الخطوات
4. افتح **Terminal** وتأكد:
   ```
   python3 --version
   ```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
python3 --version
```

---

## 2. تحميل المشروع من GitHub

افتح **Command Prompt** أو **Terminal** واكتب:

```bash
git clone https://github.com/Waleedkhadrawy/spacehub.git
```

سيتم إنشاء مجلد اسمه `spacehub` في المكان الحالي.

انتقل داخله:

```bash
cd spacehub
```

> **إذا لم يكن Git مثبتاً:**
> - Windows: حمّله من https://git-scm.com/download/win
> - macOS: شغّل `xcode-select --install` في Terminal
> - Linux: `sudo apt install git -y`

---

## 3. إنشاء البيئة الافتراضية (Virtual Environment)

البيئة الافتراضية تعزل مكتبات المشروع عن باقي مكتبات الجهاز.

### Windows:
```
python -m venv venv
```

ثم فعّلها:
```
venv\Scripts\activate
```

ستلاحظ أن الـ prompt تغيّر وأصبح في بدايته `(venv)` — هذا يعني البيئة شغّالة.

### macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

> **ملاحظة:** يجب تفعيل البيئة في كل مرة تفتح فيها نافذة جديدة قبل تشغيل المشروع.

---

## 4. تثبيت المتطلبات

تأكد أن `(venv)` ظاهر في أول السطر، ثم:

```bash
pip install -r requirements.txt
```

سيقوم بتثبيت:
- **Django** — الإطار الأساسي
- **Pillow** — معالجة الصور
- **python-dotenv** — قراءة ملف .env

انتظر حتى يكتمل، ثم تأكد:

```bash
python -m django --version
```

يجب أن يظهر رقم إصدار Django (مثلاً `4.2.x`).

---

## 5. إعداد ملف .env

المشروع يحتاج ملف `.env` يحتوي على الإعدادات السرية.

### أنشئ الملف:

**Windows (Command Prompt):**
```
copy .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

### افتح الملف بأي محرر نصوص وعدّل القيم:

افتح الملف `.env` بـ Notepad أو VS Code أو أي محرر:

```
SECRET_KEY=اكتب-هنا-أي-نص-عشوائي-طويل-مثلاً-abc123xyz456def789
DEBUG=True
CLOUDINARY_CLOUD_NAME=اتركها-فاضية-إذا-مش-هتستخدم-Cloudinary
CLOUDINARY_API_KEY=اتركها-فاضية
CLOUDINARY_API_SECRET=اتركها-فاضية
```

> **ملاحظة:** `SECRET_KEY` مهمة جداً للأمان. في بيئة التطوير (Development) يمكن وضع أي نص. لا تشاركها مع أحد في الإنتاج.

---

## 6. تشغيل قاعدة البيانات

هذه الخطوة تنشئ جداول قاعدة البيانات SQLite.

### الخطوة 6.1 — إنشاء ملفات الـ migrations:
```bash
python manage.py makemigrations
```

يجب أن تظهر:
```
Migrations for 'accounts':
  accounts\migrations\0001_initial.py
Migrations for 'spaces':
  spaces\migrations\0001_initial.py
Migrations for 'bookings':
  bookings\migrations\0001_initial.py
Migrations for 'reviews':
  reviews\migrations\0001_initial.py
```

### الخطوة 6.2 — تطبيق الـ migrations:
```bash
python manage.py migrate
```

يجب أن تظهر رسائل `OK` لكل migration:
```
Applying accounts.0001_initial... OK
Applying spaces.0001_initial... OK
Applying bookings.0001_initial... OK
Applying reviews.0001_initial... OK
```

بعد هذه الخطوة سيتم إنشاء ملف `db.sqlite3` في مجلد المشروع — هذه قاعدة البيانات.

---

## 7. إنشاء حساب المدير (Superuser)

هذا الحساب يتيح الوصول إلى لوحة إدارة Django على `/admin/`.

```bash
python manage.py createsuperuser
```

سيطلب منك:
```
Username: admin
Email address: admin@example.com
Password: (اكتب كلمة مرور - لن تظهر وهذا طبيعي)
Password (again): (أعد الكتابة للتأكيد)
Superuser created successfully.
```

> **ملاحظة:** اختر كلمة مرور لا تقل عن 8 أحرف وتحتوي على أرقام وحروف.

---

## 8. تشغيل السيرفر

```bash
python manage.py runserver
```

يجب أن يظهر:
```
Django version 4.2.x, using settings 'spacehub.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### افتح المتصفح على:

| الرابط | الوصف |
|---|---|
| http://127.0.0.1:8000/ | الصفحة الرئيسية — قائمة المساحات |
| http://127.0.0.1:8000/accounts/register/ | إنشاء حساب جديد |
| http://127.0.0.1:8000/accounts/login/ | تسجيل الدخول |
| http://127.0.0.1:8000/admin/ | لوحة إدارة Django |

### لإيقاف السيرفر:
اضغط **Ctrl + C** في نافذة الـ Terminal.

---

## 9. مشاكل شائعة وحلولها

---

### المشكلة: `python` غير معروف في Windows
```
'python' is not recognized as an internal or external command
```
**الحل:** جرّب `py` بدلاً من `python`:
```
py manage.py runserver
```
أو أعد تثبيت Python وتأكد من تفعيل "Add to PATH".

---

### المشكلة: `(venv)` لا يظهر / البيئة غير مفعّلة

**Windows:**
```
venv\Scripts\activate
```
إذا ظهر خطأ في PowerShell:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
ثم أعد تفعيل البيئة.

**macOS/Linux:**
```bash
source venv/bin/activate
```

---

### المشكلة: `ModuleNotFoundError: No module named 'django'`
يعني أنت خارج البيئة الافتراضية أو لم تثبّت المتطلبات.

**الحل:**
```bash
# فعّل البيئة أولاً
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# ثم ثبّت المتطلبات
pip install -r requirements.txt
```

---

### المشكلة: `No such file or directory: '.env'`

**الحل:** أنشئ ملف `.env`:
```bash
copy .env.example .env     # Windows
cp .env.example .env       # macOS/Linux
```

---

### المشكلة: `Port 8000 is already in use`
يعني هناك سيرفر آخر يعمل على نفس المنفذ.

**الحل:** استخدم منفذاً مختلفاً:
```bash
python manage.py runserver 8080
```
ثم افتح http://127.0.0.1:8080/

---

### المشكلة: صور لا تظهر

تأكد أن مجلد `media/` موجود في المشروع:
```bash
mkdir media     # macOS/Linux
mkdir media     # Windows
```
وتأكد أن `DEBUG = True` في ملف `.env`.

---

### المشكلة: `OperationalError: no such table`
نسيت تشغيل الـ migrations.

**الحل:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ملخص الأوامر الكاملة (للنسخ السريع)

```bash
# 1. تحميل المشروع
git clone https://github.com/Waleedkhadrawy/spacehub.git
cd spacehub

# 2. إنشاء وتفعيل البيئة الافتراضية
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 3. تثبيت المتطلبات
pip install -r requirements.txt

# 4. إعداد ملف البيئة
copy .env.example .env         # Windows
# cp .env.example .env         # macOS/Linux
# (عدّل ملف .env بأي محرر نصوص)

# 5. قاعدة البيانات
python manage.py makemigrations
python manage.py migrate

# 6. إنشاء حساب المدير
python manage.py createsuperuser

# 7. تشغيل السيرفر
python manage.py runserver
```

**ثم افتح:** http://127.0.0.1:8000/

---

## في كل مرة تشغّل المشروع من جديد

```bash
cd spacehub
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
python manage.py runserver
```

هذه الثلاث خطوات فقط كافية بعد الإعداد الأول.
