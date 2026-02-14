from fastapi import FastAPI
import routes_ml
from dotenv import load_dotenv

app = FastAPI()

app.include_router(routes_ml.router, prefix="", tags=["Machine Learning"])