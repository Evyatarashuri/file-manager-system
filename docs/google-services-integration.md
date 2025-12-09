# Google Services Integration Overview

This application integrates several Google Cloud Platform (GCP) services to build a scalable, event-driven, and resilient file-processing system. Each service was selected based on architectural fit, performance needs, and security considerations.

---

1. **Firebase Authentication**:
- Handles secure user authentication.
- Issues signed ID Tokens (JWT) which the backend verifies via Firebase Admin SDK.
- Offloads identity management, password storage, and OAuth flows to Firebase.

---

2. **Google Cloud Storage (GCS)**:
- Stores all user-uploaded files (PDF, TXT, JSON).
- Highly durable and scalable object storage.
- Allows the backend and worker to download files efficiently during processing.

---

3. **Google Pub/Sub**:
   - Acts as the message broker between the backend and worker.
   - Enables asynchronous, event-driven processing.
   - Guarantees at-least-once delivery and automatic retry of failed events.
#####   Why chosen:
   Decouples upload operations from background indexing and enables horizontal scaling.

---

4. **Google Firestore**:
   - Stores file metadata, audit logs, and the generated search_index created by the worker.
   - Schema-flexible, low-latency document database.
   - Ideal for per-user metadata and search-related data structures.
#####   Why chosen:
   I chose Firestore because it fits perfectly for storing small, flexible, document-based data.

---

5. **Google Cloud Run**:
   - Used for hosting the FastAPI backend in a serverless environment.
   - Used for hosting the React frontend in a serverless environment.
   - Supports automatic scaling and managed infrastructure.
#####   Why chosen:
   Cloud Run allows deploying containerized applications without managing servers, enabling rapid development and scaling based on demand.

---

6. **Redis Memory Store**:
   - FastAPI Backend
Handles file uploads, metadata storage, event publishing, and authentication.
   - React Frontend
Served as a standalone container, allowing full control over the build output and deployment process.

---

7. **Serverless VPC Connector**:
   - Allows Cloud Run services to communicate with Redis running inside a private VPC network.
   - Bridges serverless workloads with VPC resources.
   - Ensures secure and private connectivity.
##### Why chosen:
Cloud Run cannot reach private VPC resources (e.g., Redis VM) without this connector. 

---

8. **Compute Engine VM (Worker)**:
- Used for running the background worker that continuously listens to Pub/Sub.
- Supports long-running processes without needing an HTTP server.
- Provides stable performance for CPU-heavy text extraction and indexing.
#####   Why chosen:
Cloud Run is request-driven and shuts down when idle, but the worker must stay active 24/7 to consume messages.
A VM is the simplest and most reliable environment for running a persistent subscriber process.