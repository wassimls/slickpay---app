// 📁 server.js
import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import { MerchantInvoice } from '@slick-pay-algeria/slickpay-npm';

// 🔧 الإعدادات
dotenv.config();
const app = express();
app.use(cors());
app.use(express.json());

// 🗝️ المتغيرات من ملف البيئة
const publicKey = process.env.SLICKPAY_PUBLIC_KEY;
const sandbox = process.env.USE_SANDBOX === 'true';

const merchantInvoice = new MerchantInvoice(publicKey, sandbox);

// ✅ إنشاء الفاتورة
app.post('/api/create-invoice', async (req, res) => {
  try {
    const { amount, description } = req.body;

    const invoiceData = {
      amount: amount || 1000,
      description: description || 'طلب دفع',
      notify_url: 'https://yourdomain.com/api/payment-notify',
      back_url: 'https://yourdomain.com/thank-you',
      lang: 'ar',
    };

    const result = await merchantInvoice.store(invoiceData);

    res.json({ success: true, invoice: result });
  } catch (error) {
    console.error('فشل في إنشاء الفاتورة:', error);
    res.status(500).json({ success: false, error: 'خطأ في الخادم' });
  }
});

// 📥 استقبال إشعار الدفع
app.post('/api/payment-notify', async (req, res) => {
  const paymentInfo = req.body;

  // ⚠️ هنا تعالج الدفع وتحدث قاعدة البيانات
  console.log('📢 إشعار بالدفع من SlickPay:', paymentInfo);

  res.sendStatus(200);
});

// 🚀 تشغيل الخادم
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`✅ الخادم يعمل على http://localhost:${PORT}`);
});
