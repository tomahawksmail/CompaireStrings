# Dockerfile

# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements (if you have one) or install Flask directly
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose port 5000 (default Flask)
EXPOSE 4999

# Start the app
CMD ["gunicorn", "-b", "0.0.0.0:4999", "app:app"]