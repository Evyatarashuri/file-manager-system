# File Management System – Backend-Heavy Fullstack App (GCP / FastAPI / React)

Strong focus on: **cloud-native architecture**, **event-driven processing**, **idempotent workflows**, **Decoupled Services**, **scalability**, **reliability**, and **observability**.


The app allows authenticated users to upload, view, search, download, and delete files. Admin users can audit all files across all users with strict authorization rules.



Google Cloud Platform: 

Hosting:
- Cloud Run for serverless container hosting for the FastAPI backend.

- 

### Project Flow

# Sign-In Request Flows
Authentication (Google Sign-In) handled via **Firebase** Authentication.
- Frontend uses Firebase Auth to perform Google login.
- Firebase issues an ID token (JWT).
- Backend middleware verify_firebase_token.
- Verifies signature with Firebase public keys.


# File Upload Flow - Pub/Sub - Asynchronous Processing
1. User selects a file to upload via the React frontend (PDF / TXT / JSON).
