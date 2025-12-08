from fastapi import HTTPException

ALLOWED_TYPES = {
    "application/pdf",
    "application/json",
    "text/plain",
}

MAX_SIZE_MB = 20

def validate_file(file):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"Unsupported file type: {file.content_type}")

    file.file.seek(0, 2)  # Move to end to get size
    size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)

    if size_mb > MAX_SIZE_MB:
        raise HTTPException(400, f"File too large ({size_mb:.2f} MB). Limit is {MAX_SIZE_MB} MB.")

    return True
