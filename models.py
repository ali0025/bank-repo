from datetime import datetime
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    accounts = db.relationship('Account', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    entries = db.relationship('TransactionEntry', backref='account', lazy=True)

    @property
    def balance(self):
        # Calculate balance dynamically: (sum of debits) minus (sum of credits)
        debit_total = sum(entry.amount for entry in self.entries if entry.entry_type == 'debit')
        credit_total = sum(entry.amount for entry in self.entries if entry.entry_type == 'credit')
        return debit_total - credit_total

    def __repr__(self):
        return f"<Account {self.name}>"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    entries = db.relationship('TransactionEntry', backref='transaction', cascade="all, delete-orphan", lazy="dynamic")


    def is_balanced(self):
        # Validate that total debits equal total credits
        debit_total = sum(entry.amount for entry in self.entries if entry.entry_type == 'debit')
        credit_total = sum(entry.amount for entry in self.entries if entry.entry_type == 'credit')
        return debit_total == credit_total

    def __repr__(self):
        return f"<Transaction {self.id}>"

class TransactionEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    entry_type = db.Column(db.String(10), nullable=False)  # 'debit' or 'credit'

    def __repr__(self):
        return f"<TransactionEntry {self.id} {self.entry_type} {self.amount}>"
