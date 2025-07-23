from flask import Flask, request, jsonify
from flask_cors import CORS
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

# تحميل متغيرات البيئة
load_dotenv()

# تهيئة تطبيق Flask
app = Flask(__name__)

# تفعيل CORS (يمكن تغيير الأصول حسب الحاجة في الإنتاج)
CORS(app, resources={r"/*": {"origins": "*"}})

# إعدادات SleekPay من متغيرات البيئة
public_key = os.getenv("PUBLIC_KEY")
sandbox = os.getenv("SANDBOX", "True").lower() == "true"

# تهيئة كائنات SleekPay مع المفتاح العام ووضع السندبوكس
invoiceMerchant = InvoiceTransferMerchant(public_key, sandbox)
userAccount = Account(public_key, sandbox)
userContact = Contact(public_key, sandbox)
userTransfer = Transfer(public_key, sandbox)
userPaymentAggregation = PaymentAggregation(public_key, sandbox)
userInvoiceTransfer = InvoiceTransfer(public_key, sandbox)

@app.route("/")
def home():
    return "SleekPay Backend is running!"

# -------------------
# Merchant Account
# -------------------
@app.route("/merchant/invoices", methods=["POST"])
def create_merchant_invoice():
    try:
        data = request.get_json()
        res = invoiceMerchant.createInvoice(data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/merchant/invoices/<id>", methods=["GET"])
def get_merchant_invoice_details(id):
    try:
        res = invoiceMerchant.invoiceDetail(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/merchant/invoices", methods=["GET"])
def list_merchant_invoices():
    try:
        offset = int(request.args.get("offset", 0))
        page = int(request.args.get("page", 10))
        res = invoiceMerchant.listInvoice(offset, page)
        return jsonify(res)
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/merchant/invoices/<id>", methods=["PUT"])
def update_merchant_invoice(id):
    try:
        data = request.get_json()
        res = invoiceMerchant.updateInvoice(id, data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/merchant/invoices/<id>", methods=["DELETE"])
def delete_merchant_invoice(id):
    try:
        res = invoiceMerchant.deleteInvoice(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -------------------
# User Account
# -------------------
@app.route("/users/accounts", methods=["POST"])
def create_user_account():
    try:
        data = request.get_json()
        res = userAccount.create(data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/users/accounts/<id>", methods=["GET"])
def get_user_account_details(id):
    try:
        res = userAccount.accountDetails(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/users/accounts", methods=["GET"])
def list_user_accounts():
    try:
        offset = int(request.args.get("offset", 0))
        page = int(request.args.get("page", 10))
        res = userAccount.list(offset, page)
        return jsonify(res)
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users/accounts/<id>", methods=["PUT"])
def update_user_account(id):
    try:
        data = request.get_json()
        res = userAccount.update(id, data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/users/accounts/<id>", methods=["DELETE"])
def delete_user_account(id):
    try:
        res = userAccount.delete(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -------------------
# Contact
# -------------------
@app.route("/users/contacts", methods=["POST"])
def create_contact():
    try:
        data = request.get_json()
        res = userContact.createContact(data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/users/contacts/<id>", methods=["GET"])
def get_contact_details(id):
    try:
        res = userContact.contactDetail(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/users/contacts", methods=["GET"])
def list_contacts():
    try:
        offset = int(request.args.get("offset", 0))
        page = int(request.args.get("page", 10))
        res = userContact.listContact(offset, page)
        return jsonify(res)
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users/contacts/<id>", methods=["PUT"])
def update_contact(id):
    try:
        data = request.get_json()
        res = userContact.updateContact(id, data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/users/contacts/<id>", methods=["DELETE"])
def delete_contact(id):
    try:
        res = userContact.deleteContact(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -------------------
# Transfer
# -------------------
@app.route("/transfers/commission", methods=["POST"])
def calculate_transfer_commission():
    try:
        amount = request.get_json().get("amount")
        if not amount:
            return jsonify({"error": "Amount is required"}), 400
        res = userTransfer.calculateCommission(amount)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/transfers", methods=["POST"])
def create_transfer():
    try:
        data = request.get_json()
        res = userTransfer.createPayment(data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/transfers/<id>", methods=["GET"])
def get_transfer_details(id):
    try:
        res = userTransfer.paymentDetail(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/transfers", methods=["GET"])
def list_transfers():
    try:
        offset = int(request.args.get("offset", 0))
        page = int(request.args.get("page", 10))
        res = userTransfer.listTransfer(offset, page)
        return jsonify(res)
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/transfers/<id>", methods=["PUT"])
def update_transfer(id):
    try:
        data = request.get_json()
        res = userTransfer.updateTransfer(id, data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/transfers/<id>", methods=["DELETE"])
def delete_transfer(id):
    try:
        res = userTransfer.deleteTransfer(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -------------------
# Payment Aggregation
# -------------------
@app.route("/payment-aggregation/commission", methods=["POST"])
def calculate_commission():
    try:
        data = request.get_json()
        res = userPaymentAggregation.commission(data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/payment-aggregation", methods=["POST"])
def create_payment_aggregation():
    try:
        data = request.get_json()
        res = userPaymentAggregation.create(data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/payment-aggregation/<id>", methods=["GET"])
def get_payment_aggregation_details(id):
    try:
        res = userPaymentAggregation.details(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/payment-aggregation", methods=["GET"])
def list_payment_aggregations():
    try:
        offset = int(request.args.get("offset", 0))
        page = int(request.args.get("page", 10))
        res = userPaymentAggregation.list(offset, page)
        return jsonify(res)
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/payment-aggregation/<id>", methods=["PUT"])
def update_payment_aggregation(id):
    try:
        data = request.get_json()
        res = userPaymentAggregation.update(id, data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/payment-aggregation/<id>", methods=["DELETE"])
def delete_payment_aggregation(id):
    try:
        res = userPaymentAggregation.delete(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -------------------
# Invoice Transfer
# -------------------
@app.route("/invoice-transfers/commission", methods=["POST"])
def calculate_invoice_commission():
    try:
        amount = request.get_json().get("amount")
        if not amount:
            return jsonify({"error": "Amount is required"}), 400
        res = userInvoiceTransfer.calculateCommissionInvoice(amount)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/invoice-transfers", methods=["POST"])
def create_invoice_transfer():
    try:
        data = request.get_json()
        res = userInvoiceTransfer.createInvoice(data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/invoice-transfers/<id>", methods=["GET"])
def get_invoice_transfer_details(id):
    try:
        res = userInvoiceTransfer.InvoiceDetail(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route("/invoice-transfers", methods=["GET"])
def list_invoice_transfers():
    try:
        offset = int(request.args.get("offset", 0))
        page = int(request.args.get("page", 10))
        res = userInvoiceTransfer.listInvoice(offset, page)
        return jsonify(res)
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/invoice-transfers/<id>", methods=["PUT"])
def update_invoice_transfer(id):
    try:
        data = request.get_json()
        res = userInvoiceTransfer.updateInvoice(id, data)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/invoice-transfers/<id>", methods=["DELETE"])
def delete_invoice_transfer(id):
    try:
        res = userInvoiceTransfer.deleteInvoice(id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# لا نحتاج إلى app.run() هنا، لأن Gunicorn سيتولى التشغيل
if __name__ == "__main__":
    app.run(debug=False)