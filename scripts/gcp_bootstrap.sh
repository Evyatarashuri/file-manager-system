#!/bin/bash

set -e

PROJECT_ID="eighth-epigram-434908-k0"
BUCKET_NAME="my-file-mgmt-bucket"
TOPIC_NAME="file-uploaded"
REGION="us-central1"

echo "🔹 Setting GCP project..."
gcloud config set project $PROJECT_ID

echo "🔹 Enabling APIs..."
gcloud services enable firestore.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable pubsub.googleapis.com

echo "🔹 Creating Firestore (if not exists)..."
gcloud firestore databases create --location=$REGION --quiet || echo "Firestore already exists"

echo "🔹 Creating Bucket..."
gsutil mb -l $REGION gs://$BUCKET_NAME/ || echo "Bucket already exists"

echo "🔹 Creating Pub/Sub topic..."
gcloud pubsub topics create $TOPIC_NAME || echo "Topic exists"

echo "🔹 Creating Backend Service Account..."
gcloud iam service-accounts create backend-sa --display-name="backend"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:backend-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/datastore.user"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:backend-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:backend-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/pubsub.publisher"

echo "🔹 Generating backend JSON key..."
gcloud iam service-accounts keys create ./backend-sa.json \
  --iam-account="backend-sa@$PROJECT_ID.iam.gserviceaccount.com"

echo "🔹 EXPORT VARIABLE (temporary for shell)..."
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/backend-sa.json"

echo "🎉 DONE — GCP bootstrap successfully completed."
echo "🔥 Files / Topics / DB Ready."
