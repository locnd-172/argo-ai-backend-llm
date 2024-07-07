from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.core import settings
from src.router.chat_router import router as chat_router
from src.router.docs_router import router as docs_router
from src.router.main_router import router as main_router

app = FastAPI(title=settings.PROJECT_NAME)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(router=main_router)
app.include_router(router=chat_router)
app.include_router(router=docs_router)
