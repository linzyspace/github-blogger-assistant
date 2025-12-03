# Use slim Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app folder
COPY app ./app

# Expose the port Cloud Run will use
ENV PORT 8080
EXPOSE 8080

# Run the app with Gunicorn
# Binds to 0.0.0.0 and dynamic $PORT for Cloud Run
CMD ["sh", "-c", "gunicorn app.main:app --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0"]
