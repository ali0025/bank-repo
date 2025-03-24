# FinTrack API
## Overview
This Flask-based REST API provides a robust solution for managing personal finances using double-entry bookkeeping principles. Designed to run in a Docker container, the application offers comprehensive financial tracking with user and account management, transaction recording, and automated balance calculations.

## Features
- **User Management**: Create, retrieve, update, and delete user profiles
- **Account Management**: Create and manage financial accounts for each user
- **Double-Entry Transactions**: Record financial transactions with balanced debits and credits
- **RESTful API**: Full CRUD operations via HTTP endpoints
- **Automated Balance Calculation**: Dynamically calculate account balances from transaction entries

## Technical Stack
- **Framework**: Flask 2.2.5
- **Database ORM**: SQLAlchemy 1.4.49 (via Flask-SQLAlchemy)
- **Database**: PostgreSQL
- **Testing**: pytest
- **Containerization**: Docker

## Prerequisites
- Docker Desktop
- Git

## Installation and Setup
### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Configure Environment Variables
Create a `.env` file in the project root with the following variables:
```
POSTGRES_USER=flask_user
POSTGRES_PASSWORD=securepass123
POSTGRES_DB=flask_database_2
FLASK_DEBUG=development 
```

### 3. Start the Application
```bash
docker-compose up --build -d
```
The API will be available at `http://localhost:5000/`.

### 4. Stop the Containers
To stop the services:
```bash
docker-compose down
```

## API Endpoints
### Users
- `POST /users/`: Create a new user
- `GET /users/`: List all users
- `GET /users/<id>`: Get user details
- `PUT /users/<id>`: Update user information
- `DELETE /users/<id>`: Delete a user

### Accounts
- `POST /accounts/`: Create a new account
- `GET /accounts/`: List all accounts
- `GET /accounts/<id>`: Get account details with current balance
- `PUT /accounts/<id>`: Update account information
- `DELETE /accounts/<id>`: Delete an account

### Transactions
- `POST /transactions/`: Create a new transaction with entries
- `GET /transactions/`: List all transactions
- `GET /transactions/<id>`: Get transaction details with entries
- `PUT /transactions/<id>`: Update transaction description
- `DELETE /transactions/<id>`: Delete a transaction

## Running Tests
### Access the App Container
```bash
docker-compose exec app bash
```

### Run Tests
```bash
pytest
```

## Testing Tools
### Postman
Use Postman to test API endpoints by sending HTTP requests and inspecting responses.

### pgAdmin
Connect to the PostgreSQL database using credentials from the `.env` file to manage and explore data.

## Project Structure
```
<repository-directory>/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── extensions.py       # Database initialization
├── models.py           # Data models
├── routes.py           # API routes
├── test.py             # Test suite
├── Dockerfile          # Docker configuration for the app
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
└── .env               # Environment variables (create manually)
```

## Notes
- Ensure Docker Desktop is installed and running before starting the application or tests
- The PostgreSQL container must be healthy before the app starts
- Tests must be run inside the container to ensure the correct environment and database connection

