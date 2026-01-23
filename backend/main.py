from fastapi import FastAPI

app = FastAPI()

# test route
@app.get("/api")
def read_root():
    return {"message": "Hello from Python!"}