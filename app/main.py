<<<<<<< HEAD
from contextlib import asynccontextmanager

from fastapi import FastAPI
=======
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
>>>>>>> main

from app.config.settings import settings
from app.database.mongodb import client, db
from app.database.indexes import create_indexes
from app.routes.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    try:
        client.admin.command("ping")

<<<<<<< HEAD
        
        print("MongoDB connection successful")
        print(f"Database: {settings.DATABASE_NAME}")
       
=======
        print("========================================")
        print("MongoDB connection successful")
        print(f"Database: {settings.DATABASE_NAME}")
        print("========================================")

>>>>>>> main
        create_indexes(db)

        print("MongoDB indexes created successfully")

    except Exception as e:
<<<<<<< HEAD
        
        print("MongoDB connection failed")
        print(f"Error: {e}")
        
=======
        print("========================================")
        print("MongoDB connection failed")
        print(f"Error: {e}")
        print("========================================")
>>>>>>> main

    yield

    # Shutdown
    try:
        client.close()
        print("MongoDB connection closed")

    except Exception as e:
        print(f"Error closing MongoDB connection: {e}")

<<<<<<< HEAD
=======

>>>>>>> main
app = FastAPI(
    title=settings.APP_NAME,
    description="Restaurant Order & Kitchen Operations System",
    version="1.0.0",
    lifespan=lifespan,
)

<<<<<<< HEAD
=======
# Enable CORS for frontend UI connecting from any origin/port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

>>>>>>> main
app.include_router(
    router,
    prefix="/api",
)

<<<<<<< HEAD
@app.get("/")
def home():
=======
# Mount frontend directory for seamless standalone or integrated UI access
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend_app")


@app.get("/")
def home():
    if os.path.exists(FRONTEND_DIR):
        return RedirectResponse(url="/app/")
>>>>>>> main

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
<<<<<<< HEAD
        }
=======
        }
>>>>>>> main
