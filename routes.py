from flask import Blueprint, jsonify, request
from extensions import db
import logging
from models import User, Account, Transaction, TransactionEntry

logger = logging.getLogger(__name__)

# --- User Routes ---
user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User with provided username or email already exists"}), 400

    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    logger.info(f"User created: {user.id}")
    return jsonify({"message": "User created", "user_id": user.id}), 201

@user_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    results = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(results), 200

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    result = {"id": user.id, "username": user.username, "email": user.email}
    return jsonify(result), 200

@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    db.session.commit()
    logger.info(f"User updated: {user.id}")
    return jsonify({"message": "User updated"}), 200

@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    logger.info(f"User deleted: {user.id}")
    return jsonify({"message": "User deleted"}), 200

# --- Account Routes ---
account_bp = Blueprint("account_bp", __name__)

@account_bp.route("/", methods=["POST"])
def create_account():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")
    user_id = data.get("user_id")
    if not name or not user_id:
        return jsonify({"error": "Name and user_id are required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    account = Account(name=name, description=description, user_id=user_id)
    db.session.add(account)
    db.session.commit()
    logger.info(f"Account created: {account.id}")
    return jsonify({"message": "Account created", "account_id": account.id}), 201

@account_bp.route("/", methods=["GET"])
def get_accounts():
    accounts = Account.query.all()
    results = []
    for account in accounts:
        results.append({
            "id": account.id,
            "name": account.name,
            "description": account.description,
            "user_id": account.user_id,
            "balance": account.balance,
            "created_at": account.created_at.isoformat()
        })
    return jsonify(results), 200

@account_bp.route("/<int:account_id>", methods=["GET"])
def get_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    result = {
        "id": account.id,
        "name": account.name,
        "description": account.description,
        "user_id": account.user_id,
        "balance": account.balance,
        "created_at": account.created_at.isoformat()
    }
    return jsonify(result), 200

@account_bp.route("/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    data = request.get_json()
    account.name = data.get("name", account.name)
    account.description = data.get("description", account.description)
    db.session.commit()
    logger.info(f"Account updated: {account.id}")
    return jsonify({"message": "Account updated"}), 200

@account_bp.route("/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    db.session.delete(account)
    db.session.commit()
    logger.info(f"Account deleted: {account.id}")
    return jsonify({"message": "Account deleted"}), 200

# --- Transaction Routes ---
transaction_bp = Blueprint("transaction_bp", __name__)

@transaction_bp.route("/", methods=["POST"])
def create_transaction():
    data = request.get_json()
    description = data.get("description", "")
    entries_data = data.get("entries")
    if not entries_data or not isinstance(entries_data, list):
        return jsonify({"error": "Entries must be provided as a list"}), 400

    transaction = Transaction(description=description)
    total_debit = 0.0
    total_credit = 0.0

    for entry_data in entries_data:
        account_id = entry_data.get("account_id")
        amount = entry_data.get("amount")
        entry_type = entry_data.get("entry_type")
        if account_id is None or amount is None or entry_type not in ["debit", "credit"]:
            return jsonify({"error": "Invalid entry data"}), 400

        # Verify account existence
        from models import Account  # local import to avoid circular dependency
        account = Account.query.get(account_id)
        if not account:
            return jsonify({"error": f"Account {account_id} not found"}), 404

        entry = TransactionEntry(account_id=account_id, amount=amount, entry_type=entry_type)
        transaction.entries.append(entry)
        if entry_type == "debit":
            total_debit += amount
        else:
            total_credit += amount

    if total_debit != total_credit:
        return jsonify({"error": "Transaction is not balanced: total debit must equal total credit"}), 400

    db.session.add(transaction)
    db.session.commit()
    logger.info(f"Transaction created: {transaction.id}")
    return jsonify({"message": "Transaction created", "transaction_id": transaction.id}), 201

@transaction_bp.route("/", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.all()
    results = []
    for transaction in transactions:
        entries = []
        for entry in transaction.entries:
            entries.append({
                "id": entry.id,
                "account_id": entry.account_id,
                "amount": entry.amount,
                "entry_type": entry.entry_type
            })
        results.append({
            "id": transaction.id,
            "description": transaction.description,
            "timestamp": transaction.timestamp.isoformat(),
            "entries": entries
        })
    return jsonify(results), 200

@transaction_bp.route("/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    entries = []
    for entry in transaction.entries:
        entries.append({
            "id": entry.id,
            "account_id": entry.account_id,
            "amount": entry.amount,
            "entry_type": entry.entry_type
        })
    result = {
        "id": transaction.id,
        "description": transaction.description,
        "timestamp": transaction.timestamp.isoformat(),
        "entries": entries
    }
    return jsonify(result), 200

@transaction_bp.route("/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    data = request.get_json()
    # For simplicity, allow updating only the description.
    transaction.description = data.get("description", transaction.description)
    db.session.commit()
    logger.info(f"Transaction updated: {transaction.id}")
    return jsonify({"message": "Transaction updated"}), 200

@transaction_bp.route("/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    db.session.delete(transaction)
    db.session.commit()
    logger.info(f"Transaction deleted: {transaction.id}")
    return jsonify({"message": "Transaction deleted"}), 200
