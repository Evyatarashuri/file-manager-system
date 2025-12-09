# Architecture Overview
This system follows a cloud-native, event-driven architecture designed to handle file uploads at scale, ensure reliable background processing, and maintain a clean separation between responsibilities across services.

The workflow is designed to demonstrate backend engineering, cloud infrastructure knowledge, and real-world system design practices.

---

End-to-End File Upload & Processing Flow

1. **User Authentication**: Users authenticate through Firebase Authentication, which issues a signed ID Token (JWT).
The FastAPI backend validates this token using Firebase Admin SDK before granting access to protected endpoints.

2. **File Upload (Frontend → Backend → GCS)**:
- The React client uploads files to the FastAPI backend.
- The backend streams the file into Google Cloud Storage.
- Metadata about the file (e.g., filename, size, user ID) is stored in Firestore.

3. **Event Publication (Backend → Pub/Sub)**:
After the file is stored successfully, the backend publishes a FILE_UPLOADED event to Google Pub/Sub.
This event decouples upload operations from background processing.

4. **Background Processing (Pub/Sub → Subscriber)**:
A dedicated Worker service subscribes to the Pub/Sub topic:
- Downloads the file from GCS.
- Extracts and cleans the text (PDF, TXT, JSON).
- Builds a search_index.
- Updates Firestore with an indexed document.

5. **Search Capability**:
Once the worker finishes, the user can search their files using the React frontend, which queries Firestore for indexed documents.
