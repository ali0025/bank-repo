
# Personal Finance API

A Flask-based REST API for managing personal finances using double-entry bookkeeping principles.

## Overview

This application provides a robust API for tracking personal finances through a double-entry bookkeeping system. It allows users to create accounts, record transactions between accounts, and maintain balanced financial records.

## Features

- **User Management**: Create, retrieve, update, and delete user profiles.
- **Account Management**: Create and manage financial accounts for each user.
- **Double-Entry Transactions**: Record financial transactions with balanced debits and credits.
- **RESTful API**: Full CRUD operations via HTTP endpoints.
- **Automated Balance Calculation**: Account balances calculated dynamically from transaction entries.

## Technical Stack

- **Framework**: Flask 2.2.5
- **Database ORM**: SQLAlchemy 1.4.49 (via Flask-SQLAlchemy)
- **Database**: PostgreSQL (via psycopg2)
- **Testing**: pytest
- **Configuration**: Environment variables via python-dotenv

## Data Model

- **User**: Represents a user of the system.
- **Account**: Financial account owned by a user (e.g., checking, savings, credit card).
- **Transaction**: Record of financial activity with balanced debit and credit entries.
- **TransactionEntry**: Individual debit or credit entry linked to an account and transaction.

## API Endpoints

### Users
- `POST /users/` - Create a new user.
- `GET /users/` - List all users.
- `GET /users/<id>` - Get user details.
- `PUT /users/<id>` - Update user information.
- `DELETE /users/<id>` - Delete a user.

### Accounts
- `POST /accounts/` - Create a new account.
- `GET /accounts/` - List all accounts.
- `GET /accounts/<id>` - Get account details with current balance.
- `PUT /accounts/<id>` - Update account information.
- `DELETE /accounts/<id>` - Delete an account.

### Transactions
- `POST /transactions/` - Create a new transaction with entries.
- `GET /transactions/` - List all transactions.
- `GET /transactions/<id>` - Get transaction details with entries.
- `PUT /transactions/<id>` - Update transaction description.
- `DELETE /transactions/<id>` - Delete a transaction.

## Installation

### Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Database Setup

### Step 1: Open PostgreSQL in Terminal
Run the following command to enter the PostgreSQL interactive shell as the `postgres` user:
```bash
psql -U postgres
```

### Step 2: Create a New User
Inside the `psql` shell, create a new database user:
```sql
CREATE USER flask_user WITH PASSWORD 'securepass123';
```

### Step 3: Create a New Database
Create a new database and grant the user full control:
```sql
CREATE DATABASE flask_database_2;
GRANT ALL PRIVILEGES ON DATABASE flask_database_2 TO flask_user;
ALTER DATABASE flask_database_2 OWNER TO flask_user;
```

### Step 4: Exit PostgreSQL
Type `\q` to exit the `psql` shell.

### Step 5: Set Up the `.env` File
Create a `.env` file in your project directory and add the Database URL:
```
DATABASE_URL=postgresql://flask_user:securepass123@localhost:5432/flask_database_2
```

### Step 6: Test the Connection
Test the database connection using:
```bash
psql -U flask_user -d flask_database_2 -h localhost -W
```
Enter the password (`securepass123`). If you see the `flask_database_2=#` prompt, your setup is working.

## Running the Application

Run the Flask application:
```bash
python app.py
```
The API will be available at `http://localhost:5000/`.

## Testing

Run the tests using pytest:
```bash
pytest
```

---

