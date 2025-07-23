from flask import Flask, request, jsonify
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

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

app = Flask(__name__)

# إعدادات SleekPay
public_key = os.getenv("public_key")
sandbox = os.getenv("sandbox").lower() == "true"

# تهيئة كائنات SleekPay
invoiceMerchant = InvoiceTransferMerchant()
userAccount = Account()
userContact = Contact()
userTransfer = Transfer()
userPaymentAggregation = PaymentAggregation()
userInvoiceTransfer = InvoiceTransfer()

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

# ... (أكمل باقي الدوال بنفس الطريقة)

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

# ... (أكمل باقي الدوال بنفس الطريقة)


if __name__ == "__main__":
    app.run(debug=True)