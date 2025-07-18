# SlickPay Backend Integration 🇩🇿

هذا المشروع يمثل خادوم بسيط باستخدام Node.js و Express للتكامل مع خدمة الدفع الإلكترونية الجزائرية **SlickPay**.

## ⚙️ متطلبات التشغيل

- Node.js مثبت على جهازك
- حساب في SlickPay والحصول على المفتاح العام (Public Key)
- ملف `.env` يحتوي على مفاتيح البيئة

## 📁 الهيكل العام للمشروع

```
slickpay-backend/
├── server.js
├── package.json
├── .env
```

## 📦 تثبيت الحزم

بعد تحميل المشروع، افتح الطرفية (Terminal) داخل مجلد المشروع ونفذ:

```bash
npm install
```

## 🚀 تشغيل الخادم

```bash
npm start
```

الخادم سيكون متاحًا على:

```
http://localhost:4000/api/create-invoice
```

## 🔐 ملف البيئة `.env`

قم بإنشاء ملف باسم `.env` يحتوي على:

```
SLICKPAY_PUBLIC_KEY=أدخل_مفتاحك_هنا
USE_SANDBOX=true
```

## 🔄 إنشاء فاتورة

أرسل طلب POST إلى:

```
/api/create-invoice
```

بالمحتوى التالي:

```json
{
  "amount": 2500,
  "description": "دفع لخدمة معينة"
}
```

الرد سيكون كالتالي:

```json
{
  "success": true,
  "invoice": {
    "payment_url": "رابط صفحة الدفع"
  }
}
```

ثم يمكنك تحويل المستخدم إلى رابط `payment_url`.

## 📨 إشعارات الدفع (Webhook)

عند نجاح الدفع، ترسل SlickPay إشعارًا إلى:

```
/api/payment-notify
```

قم بمعالجة الطلب هنا (مثل تسجيل الدفع في قاعدة بياناتك).

## ✅ النشر على Vercel

1. اربط المستودع مع GitHub
2. أنشئ مشروعًا جديدًا في [https://vercel.com](https://vercel.com)
3. أضف متغيرات البيئة:
   - `SLICKPAY_PUBLIC_KEY`
   - `USE_SANDBOX`
4. اضغط **Deploy**

## 📞 دعم

لأي استفسار تقني، يمكنك التواصل مع فريق SlickPay أو طرح سؤالك هنا.
