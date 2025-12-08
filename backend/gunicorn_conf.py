import os

PORT = os.getenv("PORT", "8080")  # Cloud Run always injects 8080
bind = f"0.0.0.0:{PORT}"

workers = 2                       # Cloud Run scales instances, no need 3+
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
loglevel = "info"
