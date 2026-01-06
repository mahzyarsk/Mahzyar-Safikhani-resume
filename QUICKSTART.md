# راهنمای سریع شروع

## نصب و راه‌اندازی سریع

### 1. نصب وابستگی‌ها

```bash
cd backend
pip install -r requirements.txt
```

### 2. تنظیمات اولیه

یک فایل `.env` در پوشه `backend` ایجاد کنید:

```env
SECRET_KEY=your-very-secret-key-here-change-this
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
DATABASE_URL=sqlite:///./resume.db
```

### 3. اجرای سرور

```bash
cd backend
python main.py
```

یا:

```bash
python run.py
```

سرور روی `http://localhost:8000` اجرا می‌شود.

### 4. تست API

- مستندات Swagger: http://localhost:8000/docs
- صفحه ادمین: http://localhost:8000/admin
- API Root: http://localhost:8000

### 5. تنظیم فرانت‌اند

در فایل `index.html`، خط زیر را پیدا کرده و آدرس سرور را تغییر دهید:

```javascript
const API_BASE = 'http://localhost:8000';  // آدرس سرور خود را قرار دهید
```

برای production، آدرس سرور واقعی را قرار دهید، مثلاً:
```javascript
const API_BASE = 'https://your-backend-domain.com';
```

## استفاده از پنل مدیریت

1. به آدرس `http://localhost:8000/admin` بروید
2. با نام کاربری و رمز عبور از فایل `.env` وارد شوید
3. درخواست‌های پروژه را مشاهده و مدیریت کنید

## تست WebSocket

1. صفحه رزومه را در چند تب مرورگر باز کنید
2. تعداد کاربران آنلاین باید به صورت زنده به‌روزرسانی شود

## دیپلوی

### GitHub Pages (فرانت‌اند)

1. پروژه را در GitHub push کنید
2. Settings > Pages > Source را روی main branch تنظیم کنید
3. آدرس نهایی: `https://<username>.github.io/<repo-name>`

### لیارا (بک‌اند)

1. پروژه را در GitHub قرار دهید
2. در لیارا، پروژه جدید ایجاد کنید
3. از GitHub متصل کنید
4. متغیرهای محیطی را تنظیم کنید
5. دیپلوی کنید

## نکات مهم

- ✅ در production حتماً `SECRET_KEY` قوی استفاده کنید
- ✅ رمز عبور ادمین را تغییر دهید
- ✅ CORS را محدود کنید (در `main.py`)
- ✅ از HTTPS استفاده کنید
- ✅ برای production از PostgreSQL استفاده کنید

