import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.admin import require_admin
from app.config.firebase import init_firebase

# Routers
from app.api.routes.files import router as files_router
from app.api.routes.auth import router as auth_router
from app.api.routes.search import router as search_router
from app.api.routes.admin import router as admin_router

#############################
# ENV MODE SELECTION
#############################
ENV_MODE = os.getenv("ENV", "DEV").upper()

# Only initialize firebase if credentials available
if ENV_MODE != "PROD" or os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    init_firebase()
else:
    print("Firebase disabled – no credentials found (Cloud Run safe mode)")

def setup_app():
    # ========== PROD MODE ==========
    if ENV_MODE == "PROD":
        return FastAPI(
            title="File Manager API",
            docs_url=None,
            redoc_url=None,
            openapi_url=None
        )

    # ========== ADMIN ONLY DOCS ==============
    if ENV_MODE == "ADMIN_ONLY":
        from fastapi.openapi.docs import get_swagger_ui_html
        from fastapi.openapi.utils import get_openapi
        
        app = FastAPI(title="Secure File Manager API",
                      docs_url=None, redoc_url=None, openapi_url=None)

        @app.get("/secure-docs", dependencies=[Depends(require_admin)])
        def secure_docs():
            return get_swagger_ui_html(openapi_url="/secure-openapi", title="Admin Docs")

        @app.get("/secure-openapi", dependencies=[Depends(require_admin)])
        def secure_openapi():
            return get_openapi(title="File Manager API Secure", version="1.0.0", routes=app.routes)

        return app

    # ========== DEV MODE ==========
    return FastAPI(
        title="File Manager API (DEV MODE)",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )


# Initialize The App
app = setup_app()


#############################
# CORS
#############################
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#############################
# ROUTES
#############################
app.include_router(auth_router, prefix="/auth")
app.include_router(files_router, prefix="/files")
app.include_router(search_router, prefix="/search")
app.include_router(admin_router, prefix="/admin")

@app.get("/")
def root():
    return {"status": "backend running", "mode": ENV_MODE}
