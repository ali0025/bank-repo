from flask import Flask
from config import Config
from extensions import db
import os
# Register blueprints
from routes import account_bp, transaction_bp, user_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
from routes import account_bp, transaction_bp, user_bp

app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(account_bp, url_prefix="/accounts")
app.register_blueprint(transaction_bp, url_prefix="/transactions")
# Add a root route
@app.route('/')
def home():
    return {"message": "Welcome to the Flask API!"}, 200

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
    debug = os.getenv('FLASK_DEBUG') == 'development'
    app.run(host="0.0.0.0", port=5000, debug=debug)
