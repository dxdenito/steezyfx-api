from fastapi import FastAPI

from app.api.v1.routes.auth import router as auth_router

app = FastAPI()


app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome! Steezy fx api is running!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
