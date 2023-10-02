import os
import json

from fastapi import FastAPI
from dotenv import load_dotenv

from backend.api.service.db_service import DatabaseService
from backend.api.router import user_router
from backend.api.router import product_router


env = os.environ.get
load_dotenv('./.env')

ADMINS = json.loads(env('ADMINS'))

DEBUG = (env('DEBUG').lower()=="true")
POSTGRE_CON = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}" \
              f"@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"

tags_metadata = [
    {
        "name": "Taipex data",
        "description": "CRUD operations with **products / users**",
    },
    {
        "name": "User",
        "description": "telegram user crud operations (admin rights included) 🌐",
        "externalDocs": {
            "description": "Telegram",
            "url": "https://t.me/Taipexbot",
        },
    },
    {
        "name": "Product",
        "description": "product crud operations (admin rights included) ☕",
    },
]

app = FastAPI(
    title="Taipex API",
    summary="Chilled api service for a small market 🐍",
    description="Telegram web application to manage basic product line management. CRUD operations with **products / users**",
    contact={
        "name": "Segfaul",
        "url": "https://github.com/segfaul",
    },
    openapi_tags=tags_metadata
)

db_service = DatabaseService(DEBUG, POSTGRE_CON, ADMINS)


app.include_router(user_router.router)
app.include_router(product_router.router)


@app.on_event("startup")
async def startup() -> None:
    await db_service.init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    await db_service.close_db()
