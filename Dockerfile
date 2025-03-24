FROM python:3.11-slim

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y postgresql-client
# Set working directory
WORKDIR /app

# Copy files to container
COPY requirements.txt .
COPY . .

# Install dependencies
RUN pip install -r requirements.txt && pip install python-dotenv

# Set environment variables
ENV FLASK_APP=app.py

# Expose Flask port
EXPOSE 5000

# Run Flask app
# Default command to run the application
CMD ["python", "app.py"]