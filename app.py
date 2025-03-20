from flask import Flask
from config import Config
from extensions import db
# Register blueprints
from routes import account_bp, transaction_bp, user_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
from routes import account_bp, transaction_bp, user_bp

app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(account_bp, url_prefix="/accounts")
app.register_blueprint(transaction_bp, url_prefix="/transactions")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)
