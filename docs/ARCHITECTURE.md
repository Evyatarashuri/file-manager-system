# Architecture Overview
This system follows a cloud-native, event-driven architecture designed to handle file uploads at scale, ensure reliable background processing, and maintain a clean separation between responsibilities across services.

The workflow is designed to demonstrate backend engineering, cloud infrastructure knowledge, and real-world system design practices.

---

## End-to-End File Upload & Processing Flow

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

---

## Distributed Architecture Rationale

**Why I Chose a Distributed Architecture**

I designed the system as a distributed, event-driven architecture rather than a monolithic service because it provides several advantages:

1. **Decoupling**: Each component (frontend, backend, worker) has a single responsibility. This makes the system easier to maintain and extend. And can scale or fail separately.

2. **Scalability**: Components can be scaled independently based on load. For example, if file uploads spike, I can scale the backend without affecting the worker service.

3. **Resilience**: Using Pub/Sub for event-driven processing allows for retries and fault tolerance. If the worker fails to process a file, the message remains in the queue for later retry.

4. **Asynchronous processing**: heavy tasks such as text extraction and indexing do not block the user’s upload flow.

**Why Pub/Sub**

Google Pub/Sub provides a reliable event-driven backbone for the system:

- Asynchronous communication between services
- Automatic retry on failures
- High throughput and horizontal scalability
- Buffering of events during worker downtime
- Loose coupling between upload API and indexing worker

This allows the backend to remain responsive even under high load.

**Trade-offs of Distributed Systems (and how I solved them)**

Distributed architectures introduce challenges that do not exist in monolithic systems.
I handled these challenges explicitly in my design.

1. **At-Least-Once Delivery (duplicate events)**
Pub/Sub may deliver the same event more than once.

Solution:
I implemented a Redis-based distributed lock (index:<file_id>) that ensures only one worker can index a file.
Even if multiple identical events arrive, only the worker that acquires the lock processes the file; others skip or return cached results.

2. **Race Conditions & Concurrency Collisions**
Multiple workers may try to index the same file simultaneously (due to retries or duplicates).

Solution:
The Redis lock prevents concurrent processing of the same file_id.
Additionally, successful indexing is cached so that duplicate events return the existing result instead of re-running heavy processing.

3. **Eventual Consistency**
In a distributed system, the upload and indexing stages do not complete at the same time.
A file may be uploaded before its search index is ready.

Future Solution:
Files start with indexed: false and are updated once the worker completes indexing.
The frontend and API handle this state gracefully (e.g., showing “Processing” until indexing completes).

4. **Worker Failures**
A worker may crash mid-processing, leaving a file in an inconsistent state.

Solution:
Redis locks have a TTL.
If a worker crashes, the lock automatically expires, allowing another worker to retry safely.

---

## Layered Architecture (API → Service → Repository)

**The project uses a simple three-layer architecture:**

**API Layer** – Handles HTTP requests, routing, validation, and auth.

**Service Layer** – Contains business logic and workflows.

**Repository Layer** – Integrates with external systems (Firestore, Storage, Redis, Pub/Sub).

**Why this structure?**

**SRP (Single Responsibility Principle)**
Each layer has one clear responsibility → cleaner, more maintainable code.

**DIP (Dependency Inversion Principle)**
The service layer depends on abstract repositories, not on Firestore/GCS directly.
This makes it easy to switch infrastructure (e.g., Firestore → MongoDB) without touching business logic.

**Easier testing**
Repositories can be mocked, services can be tested independently, and API tests don’t require hitting real cloud services.

---

## Future Enhancements

1. **CDN Integration**: Serve files via a CDN for faster global access.

2. **Pagination**: Implement pagination for file listings.

3. **Monitoring & Alerts**: Integrate monitoring tools (e.g., Stackdriver) for real-time alerts on system health.

4. **Advanced Search**: Implement full-text search capabilities using a dedicated search engine (e.g., Elasticsearch).

5. **API Gateway**: Introduce an API Gateway to centralize authentication, rate limiting, routing, and security.

6. **Dead-Letter Queue**: Add a DLQ to isolate failed Pub/Sub messages and improve reliability.