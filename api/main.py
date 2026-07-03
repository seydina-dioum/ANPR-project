from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

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

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

from api.routers import detect
app.include_router(detect.router, prefix="/api", tags=["Détection"])

@app.get("/health", tags=["Santé"])
def health():
    return {"status": "ok", "service": "ANPR Sénégal"}

@app.get("/", response_class=HTMLResponse)
async def interface(request: Request):
    return templates.TemplateResponse(request, "index.html")
