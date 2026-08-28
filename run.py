import os
from flask import Flask
from flask_cors import CORS
from extensions import db
from models import Customer

def create_app():
    market = Flask(__name__)
    
    # Enable CORS security profiles
    CORS(market, resources={r"/*": {"origins": "*", "allow_headers": "*", "methods": ["GET", "POST", "OPTIONS"]}})

    # Dynamic database evaluation check
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    market.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///market.db'
    market.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect tools
    db.init_app(market)

    # 🔗 NEW ADDITION: Register your separate routes file blueprint directly into the app context!
    from routes import customer_bp
    market.register_blueprint(customer_bp)

    with market.app_context():
        db.create_all()

    return market


if __name__ == '__main__':
    # Start your local server instance
    create_app().run(port=5000, debug=True)

