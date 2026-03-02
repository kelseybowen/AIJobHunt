from fastapi import FastAPI
from . import routes_ml
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.include_router(routes_ml.router, prefix="/ml", tags=["Machine Learning"])

@app.get("/")
def read_root():
    return {"message": "ML Service is running"}