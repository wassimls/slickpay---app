from flask import Flask, request, jsonify
from flask_cors import CORS  # استيراد مكتبة CORS
from dotenv import load_dotenv
import os
from slickpay import (
    InvoiceTransferMerchant,
    Account,
    Contact,
    Transfer,
    PaymentAggregation,
    InvoiceTransfer,
)

# تحميل متغيرات البيئة (يعمل فقط في البيئة المحلية)
load_dotenv()

# تهيئة تطبيق Flask
app = Flask(__name__)

# تفعيل CORS للسماح بالطلبات من أي مصدر (يمكنك تخصيصه لاحقًا لنطاق موقعك فقط)
CORS(app)

# إعدادات SleekPay من متغيرات البيئة
public_key = os.getenv("public_key")
sandbox = os.getenv("sandbox", "True").lower() == "true"

# تهيئة كائنات SleekPay
invoiceMerchant = InvoiceTransferMerchant()
userAccount = Account()
userContact = Contact()
userTransfer = Transfer()
userPaymentAggregation = PaymentAggregation()
userInvoiceTransfer = InvoiceTransfer()

@app.route("/")
def home():
    return "SleekPay Backend is running!"

# -------------------
# Merchant Account
# -------------------
@app.route("/merchant/invoices", methods=["POST"])
def create_merchant_invoice():
    data = request.get_json()
    res = invoiceMerchant.createInvoice(data)
    return jsonify(res)

@app.route("/merchant/invoices/<id>", methods=["GET"])
def get_merchant_invoice_details(id):
    res = invoiceMerchant.invoiceDetail(id)
    return jsonify(res)

@app.route("/merchant/invoices", methods=["GET"])
def list_merchant_invoices():
    offset = request.args.get("offset", 0)
    page = request.args.get("page", 10)
    res = invoiceMerchant.listInvoice(offset, page)
    return jsonify(res)

# ... أكمل باقي الدوال بنفس الطريقة التي كانت عليها ...

# -------------------
# User Account
# -------------------
@app.route("/users/accounts", methods=["POST"])
def create_user_account():
    data = request.get_json()
    res = userAccount.create(data)
    return jsonify(res)

@app.route("/users/accounts/<id>", methods=["GET"])
def get_user_account_details(id):
    res = userAccount.accountDetails(id)
    return jsonify(res)

# ... أكمل باقي دوال المستخدم بنفس الطريقة ...


# لا نحتاج إلى app.run() هنا، لأن Gunicorn سيتولى التشغيل