from fastapi import FastAPI

from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.post import router as post_router
from app.api.v1.routes.category import router as category_router
from app.api.v1.routes.tag import router as tag_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(post_router)
app.include_router(category_router)
app.include_router(tag_router)


@app.get("/")
def read_root():
    return {"message": "Welcome! Steezy fx api is running!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
