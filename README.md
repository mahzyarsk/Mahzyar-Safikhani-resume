# رزومه آنلاین تعاملی

پروژه رزومه آنلاین تعاملی با قابلیت ثبت درخواست پروژه، مدیریت درخواست‌ها و نمایش تعداد کاربران آنلاین به صورت زنده.

## ویژگی‌ها

- ✅ صفحه رزومه با طراحی زیبا و واکنش‌گرا
- ✅ فرم ثبت درخواست پروژه
- ✅ پنل مدیریت با احراز هویت JWT
- ✅ نمایش تعداد کاربران آنلاین با WebSocket
- ✅ API کامل با مستندات Swagger

## ساختار پروژه

```
.
├── index.html          # صفحه اصلی رزومه
├── style.css           # استایل‌های صفحه رزومه
├── backend/
│   ├── main.py        # سرور FastAPI
│   ├── admin.html     # صفحه مدیریت
│   ├── requirements.txt
│   └── .env.example   # نمونه فایل تنظیمات
└── README.md
```

## نصب و راه‌اندازی

### 1. راه‌اندازی بک‌اند

```bash
cd backend
pip install -r requirements.txt
```

### 2. تنظیمات

فایل `.env` را از `.env.example` کپی کنید و تنظیمات را تغییر دهید:

```bash
cp .env.example .env
```

سپس فایل `.env` را ویرایش کنید و `SECRET_KEY` و اطلاعات ادمین را تغییر دهید.

### 3. اجرای سرور

```bash
python main.py
```

یا با uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

سرور روی آدرس `http://localhost:8000` اجرا می‌شود.

### 4. مستندات API

پس از اجرای سرور، مستندات Swagger در آدرس زیر در دسترس است:

```
http://localhost:8000/docs
```

## استفاده

### صفحه رزومه

صفحه رزومه شامل:
- اطلاعات شخصی
- مهارت‌ها
- سوابق تحصیلی و کاری
- فرم ثبت درخواست پروژه
- نمایش تعداد کاربران آنلاین

**نکته:** قبل از استفاده، آدرس API را در فایل `index.html` تغییر دهید:

```javascript
const API_BASE = 'http://localhost:8000';  // آدرس سرور خود را قرار دهید
```

### پنل مدیریت

برای دسترسی به پنل مدیریت:

1. به آدرس `/admin` بروید
2. با اطلاعات ادمین (از فایل `.env`) وارد شوید
3. درخواست‌ها را مشاهده و مدیریت کنید

امکانات پنل مدیریت:
- مشاهده تمام درخواست‌ها
- تغییر وضعیت درخواست‌ها
- حذف درخواست‌ها
- آمار کلی درخواست‌ها

## API Endpoints

### عمومی

- `POST /api/requests` - ثبت درخواست پروژه جدید
- `GET /api/online-count` - دریافت تعداد کاربران آنلاین
- `WebSocket /ws` - اتصال برای دریافت تعداد کاربران آنلاین به صورت زنده

### نیازمند احراز هویت

- `GET /api/requests` - دریافت لیست تمام درخواست‌ها
- `GET /api/requests/{id}` - دریافت جزئیات یک درخواست
- `PATCH /api/requests/{id}/status` - تغییر وضعیت درخواست
- `DELETE /api/requests/{id}` - حذف درخواست

### احراز هویت

- `POST /api/auth/login` - ورود و دریافت توکن JWT

## دیپلوی

### GitHub Pages (فرانت‌اند)

1. پروژه را در GitHub منتشر کنید
2. در تنظیمات Repository، بخش Pages را فعال کنید
3. آدرس نهایی: `https://<username>.github.io/<repository-name>`

**نکته:** پس از دیپلوی، آدرس API را در `index.html` به آدرس سرور واقعی تغییر دهید.

### دیپلوی بک‌اند

#### لیارا (Liara)

1. حساب کاربری در لیارا ایجاد کنید
2. پروژه را در GitHub قرار دهید
3. در لیارا، پروژه جدید ایجاد کنید و از GitHub متصل کنید
4. متغیرهای محیطی را در تنظیمات تنظیم کنید
5. پس از دیپلوی، آدرس سرور را در فایل `index.html` قرار دهید

#### VPS

1. سرور را با Python 3.8+ تنظیم کنید
2. پروژه را کلون کنید
3. وابستگی‌ها را نصب کنید
4. با استفاده از systemd یا supervisor سرویس را اجرا کنید
5. از nginx به عنوان reverse proxy استفاده کنید

مثال systemd service:

```ini
[Unit]
Description=Resume Backend API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

## امنیت

- در production حتماً `SECRET_KEY` قوی و تصادفی استفاده کنید
- رمز عبور ادمین را تغییر دهید
- CORS را محدود کنید (در `main.py` تنظیمات `allow_origins` را تغییر دهید)
- از HTTPS استفاده کنید
- برای دیتابیس production از PostgreSQL استفاده کنید

## تکنولوژی‌ها

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Backend:** FastAPI, Python
- **Database:** SQLite (توسعه) / PostgreSQL (production)
- **Authentication:** JWT
- **Real-time:** WebSocket
- **Deployment:** GitHub Pages (Frontend), Liara/VPS (Backend)

## مجوز

این پروژه برای استفاده آموزشی و شخصی است.

## تماس

- ایمیل: Mahzyar.safikhani@gmail.com
- GitHub: [mahzyarsk](https://github.com/mahzyarsk)

