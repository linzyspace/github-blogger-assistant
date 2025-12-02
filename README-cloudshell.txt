#!/bin/bash
# deploy_full.sh — Test Flask locally, build Docker, deploy to Cloud Run

SERVICE_NAME="github-blogger-assistant"
REGION="us-central1"
IMAGE_NAME="gcr.io/$GOOGLE_CLOUD_PROJECT/$SERVICE_NAME"
PORT=8080

# -----------------------------
# 1️⃣ Test Flask app locally
# -----------------------------
echo "Step 1: Testing Flask app locally..."
if python3 -m pip install -r requirements.txt; then
    echo "Dependencies installed."
else
    echo "⚠ Failed to install dependencies. Check requirements.txt"
    exit 1
fi

echo "Running Flask app in test mode..."
export PORT=$PORT
python3 app/main.py &
FLASK_PID=$!
sleep 5

# Test if Flask started
if nc -z localhost $PORT; then
    echo "✅ Flask app is running locally on port $PORT."
else
    echo "❌ Flask app failed to start. Check your modules or app structure."
    kill $FLASK_PID
    exit 1
fi
kill $FLASK_PID
echo "Stopped local Flask test."

# -----------------------------
# 2️⃣ Build Docker container
# -----------------------------
echo "Step 2: Building Docker container..."
docker build -t "$IMAGE_NAME" .

# -----------------------------
# 3️⃣ Test Docker container locally
# -----------------------------
echo "Step 3: Running Docker container locally..."
docker run -d -e PORT=$PORT -p $PORT:$PORT --name temp-app "$IMAGE_NAME"
sleep 5
if nc -z localhost $PORT; then
    echo "✅ Docker container started successfully on port $PORT."
else
    echo "❌ Docker container failed. Check Dockerfile or app structure."
    docker logs temp-app
    docker rm -f temp-app
    exit 1
fi
docker rm -f temp-app
echo "Stopped local Docker test."

# -----------------------------
# 4️⃣ Deploy to Cloud Run
# -----------------------------
echo "Step 4: Deploying to Cloud Run..."
gcloud builds submit --tag "$IMAGE_NAME"
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE_NAME" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated

# -----------------------------
# 5️⃣ Output service URL
# -----------------------------
echo "✅ Deployment complete! Your Cloud Run URL:"
gcloud run services describe "$SERVICE_NAME" \
  --region "$REGION" \
  --platform managed \
  --format "value(status.url)"
