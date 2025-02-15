import os
from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import router
from .admin_routes import admin_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(admin_router)


@app.get("/")
def read_root():
    return {"message": "인증 서비스 작동 중"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8000)