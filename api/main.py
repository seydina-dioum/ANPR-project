from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ANPR Sénégal",
    description="API reconnaissance automatique de plaques sénégalaises",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routers import detect
app.include_router(detect.router, prefix="/api", tags=["Détection"])

@app.get("/health", tags=["Santé"])
def health():
    return {"status": "ok", "service": "ANPR Sénégal"}