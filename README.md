# File Management System – Backend-Heavy Fullstack App (GCP / FastAPI / React)
---


# System Architecture Diagrams

Below is the visual overview of the system’s high-level architecture, file-processing pipeline, and authentication flow.

---

## Asynchronous File Processing & Search Indexing Pipeline

This diagram illustrates the end-to-end flow of file uploads, metadata storage, Pub/Sub event publishing, worker processing, Redis coordination, and Firestore indexing.

![Asynchronous File Processing Pipeline](docs/file-processing.svg)

---

## Firebase Authentication Flow (Frontend → Backend → Firebase)

This diagram shows how the frontend signs in via Firebase, sends an ID Token to the backend, and how the backend verifies the token using Firebase Admin SDK.

![Firebase Authentication Flow](docs/firebase-auth-flow.svg)

---

## Additional Documentation

You can find extended explanations inside:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/google-services-integration.md`](docs/google-services-integration.md)


---


## Local Setup Instructions (Work in Progress)
This README is still under construction — a complete local setup guide will be added soon.