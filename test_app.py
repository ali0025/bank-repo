import pytest
from flask import Flask
from extensions import db
from dotenv import load_dotenv
from models import User, Account, Transaction, TransactionEntry
from routes import user_bp, account_bp, transaction_bp
import os
load_dotenv()
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["TESTING"] = True
    db.init_app(app)
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(account_bp, url_prefix="/accounts")
    app.register_blueprint(transaction_bp, url_prefix="/transactions")
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

# --- User Routes ---
def test_create_user(client):
    response = client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 201
    assert "user_id" in response.json

def test_get_users(client):
    response = client.get("/users/")
    assert response.status_code == 200

def test_get_user(client):
    client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    response = client.get("/users/1")
    assert response.status_code == 200

def test_update_user(client):
    client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    response = client.put("/users/1", json={"username": "updateduser"})
    assert response.status_code == 200

def test_delete_user(client):
    client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    response = client.delete("/users/1")
    assert response.status_code == 200

# --- Account Routes ---
def test_create_account(client):
    client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    response = client.post("/accounts/", json={"name": "Test Account", "user_id": 1})
    assert response.status_code == 201
    assert "account_id" in response.json

def test_get_accounts(client):
    response = client.get("/accounts/")
    assert response.status_code == 200

def test_get_account(client):
    client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    client.post("/accounts/", json={"name": "Test Account", "user_id": 1})
    response = client.get("/accounts/1")
    assert response.status_code == 200

def test_update_account(client):
    client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    client.post("/accounts/", json={"name": "Test Account", "user_id": 1})
    response = client.put("/accounts/1", json={"name": "Updated Account"})
    assert response.status_code == 200

def test_delete_account(client):
    client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    client.post("/accounts/", json={"name": "Test Account", "user_id": 1})
    response = client.delete("/accounts/1")
    assert response.status_code == 200

# --- Transaction Routes ---
def test_create_transaction(client):
    client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    client.post("/accounts/", json={"name": "Account1", "user_id": 1})
    client.post("/accounts/", json={"name": "Account2", "user_id": 1})
    transaction_data = {
        "description": "Test Transaction",
        "entries": [
            {"account_id": 1, "amount": 100, "entry_type": "debit"},
            {"account_id": 2, "amount": 100, "entry_type": "credit"}
        ]
    }
    response = client.post("/transactions/", json=transaction_data)
    assert response.status_code == 201

def test_get_transactions(client):
    response = client.get("/transactions/")
    assert response.status_code == 200

def test_get_transaction(client):
    client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    client.post("/accounts/", json={"name": "Account1", "user_id": 1})
    client.post("/accounts/", json={"name": "Account2", "user_id": 1})
    client.post("/transactions/", json={
        "description": "Test Transaction",
        "entries": [
            {"account_id": 1, "amount": 100, "entry_type": "debit"},
            {"account_id": 2, "amount": 100, "entry_type": "credit"}
        ]
    })
    response = client.get("/transactions/1")
    assert response.status_code == 200

def test_delete_transaction(client):
    client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    client.post("/accounts/", json={"name": "Account1", "user_id": 1})
    client.post("/accounts/", json={"name": "Account2", "user_id": 1})
    client.post("/transactions/", json={
        "description": "Test Transaction",
        "entries": [
            {"account_id": 1, "amount": 100, "entry_type": "debit"},
            {"account_id": 2, "amount": 100, "entry_type": "credit"}
        ]
    })
    response = client.delete("/transactions/1")
    assert response.status_code == 200
