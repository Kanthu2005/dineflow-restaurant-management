from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import settings
from app.database.mongodb import client, db
from app.database.indexes import create_indexes
from app.routes.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    try:
        client.admin.command("ping")

        
        print("MongoDB connection successful")
        print(f"Database: {settings.DATABASE_NAME}")
       
        create_indexes(db)

        print("MongoDB indexes created successfully")

    except Exception as e:
        
        print("MongoDB connection failed")
        print(f"Error: {e}")
        

    yield

    # Shutdown
    try:
        client.close()
        print("MongoDB connection closed")

    except Exception as e:
        print(f"Error closing MongoDB connection: {e}")

app = FastAPI(
    title=settings.APP_NAME,
    description="Restaurant Order & Kitchen Operations System",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    router,
    prefix="/api",
)

@app.get("/")
def home():

    return {
        "message": "Restaurant Management System API is running",
        "database": "MongoDB",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():

    try:

        client.admin.command("ping")

        return {
            "status": "healthy",
            "database": "MongoDB",
            "database_name": settings.DATABASE_NAME,
        }

    except Exception as e:

        return {
            "status": "unhealthy",
            "database": "MongoDB",
            "error": str(e),
        }