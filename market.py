from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

market = Flask(__name__)

CORS(market, resources={r"/*": {"origins": "*", "allow_headers": "*", "methods": ["GET", "POST", "OPTIONS"]}})

# 1. ADDED: Tell Flask where to create your local database file
market.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
market.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(market)

# Define your Database Table Structure
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    payment = db.Column(db.String(100), nullable=False)

    # Helper method to instantly turn a database row into a dictionary for JSON output
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "payment": self.payment
        }

# Automatically creates the 'market.db' file if it doesn't exist yet
with market.app_context():
    db.create_all()

# --- ENDPOINTS ---

@market.route('/customers', methods=['GET'])
def display_all():
    # 2. CHANGED: Query all customers from the database table
    all_customers = Customer.query.all()
    
    # Convert every customer object row into a dictionary list
    customer_list = [customer.to_dict() for customer in all_customers]
    
    return jsonify({"status": "success", "data": customer_list})

@market.route('/customers/<int:cus_id>', methods=['GET'])
def display_by_id(cus_id):
    # 3. CHANGED: Fetch the customer directly by its primary key ID
    customer = Customer.query.get(cus_id)
    
    if customer is None:
        return jsonify({"error": "customer not found"}), 404
        
    return jsonify(customer.to_dict()), 200

@market.route('/customers', methods=['POST'])
def create_customer():
    # 1. Grab incoming network fields safely
    name = request.json.get('name')
    date = request.json.get('date')
    payment = request.json.get('payment')

    # 2. ADDED: Defensive Validation Check
    # Verify that the payment value is a clean numeric digit (no letters or symbols)
    if payment and not str(payment).isdigit():
        return jsonify({"error": "Bad Request: Payment must be a clean numeric digit format."}), 400

    # 3. Build and append rows payload permanently to your SQL schema if safe
    new_cus = Customer(
        name=name,
        date=date,
        payment=payment
    )

    db.session.add(new_cus)
    db.session.commit()
    
    return jsonify(new_cus.to_dict()), 201

@market.route('/customers/<int:cus_id>', methods=['DELETE'])
def delete_customer(cus_id):
    # Search the table directly by its primary key ID
    customer = Customer.query.get(cus_id)
    
    if customer is None:
        return jsonify({"error": "Data Error: Customer row record not found"}), 404
        
    # Erase the row from the tracking layer and commit changes to disk
    db.session.delete(customer)
    db.session.commit()
    
    return jsonify({"message": f"Customer row {cus_id} successfully deleted from table."}), 200


if __name__ == '__main__':
    market.run(port=5000, debug=True)
