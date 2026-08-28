from flask import Blueprint, jsonify, request, send_from_directory
from extensions import db
from models import Customer
import os
# 1. Create an independent Flask Blueprint container named 'customer_bp'
customer_bp = Blueprint('customer_bp', __name__)

# 2. THE READ ENDPOINT (GET)
@customer_bp.route('/customers', methods=['GET'])
def display_all():
    all_customers = Customer.query.all()
    customer_list = [customer.to_dict() for customer in all_customers]
    return jsonify({"status": "success", "data": customer_list})

# 3. THE CREATE ENDPOINT (POST)
@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    name = request.json.get('name')
    date = request.json.get('date')
    payment = request.json.get('payment')

    # Security input validation check to defend database integrity
    if payment and not str(payment).isdigit():
        return jsonify({"error": "Bad Request: Payment must be a clean numeric digit format."}), 400

    new_cus = Customer(name=name, date=date, payment=payment)
    db.session.add(new_cus)
    db.session.commit()
    return jsonify(new_cus.to_dict()), 201

# 4. THE DELETE ENDPOINT (DELETE)
@customer_bp.route('/customers/<int:cus_id>', methods=['DELETE'])
def delete_customer(cus_id):
    customer = Customer.query.get(cus_id)
    if customer is None:
        return jsonify({"error": "Data Error: Customer row record not found"}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer row {cus_id} successfully deleted from table."}), 200

@customer_bp.route('/')
def serve_index_page():
    # Find the exact path of the static folder on your computer
    static_folder_path = os.path.join(os.getcwd(), 'static')
    
    # Safely locate index.html inside the static folder and send it to the browser
    return send_from_directory(static_folder_path, 'index.html')