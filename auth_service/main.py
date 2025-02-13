import os
from fastapi import FastAPI
from .database import engine, Base
from . import models


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "auth service running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8000)