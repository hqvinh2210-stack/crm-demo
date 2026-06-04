from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.config import settings
from app.database import Base, engine
from app.routers import ai, auth, customers, conversations, integrations, messages, webhook

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRM Backend",
    description="CRM backend với webhook layer, PostgreSQL, Redis và AI agent",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(",") if isinstance(settings.ALLOWED_ORIGINS, str) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["xác thực"])
app.include_router(customers.router, prefix="/customers", tags=["khách hàng"])
app.include_router(conversations.router, prefix="/conversations", tags=["cuộc trò chuyện"])
app.include_router(messages.router, prefix="/messages", tags=["tin nhắn"])
app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
app.include_router(integrations.router, prefix="/integrations", tags=["tích hợp"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])

@app.get("/")
def root():
    base = Path(__file__).resolve().parents[1]
    frontend_file = base / "frontend" / "index.html"
    static_file = Path(__file__).resolve().parent / "static" / "index.html"
    if frontend_file.exists():
        return FileResponse(frontend_file)
    return FileResponse(static_file)
