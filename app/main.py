from fastapi import FastAPI
from sqlalchemy import text
app = FastAPI(title="Resta API")

@app.get("/")
def home():
    return {"message": "Resta API is running"}

@app.get("/db-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database": result.scalar()}