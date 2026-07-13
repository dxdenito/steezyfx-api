from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth_schema import UserCreate, UserLogin, UserOut, TokenResponse
from app.core.database import get_db

from app.repositories.auth_repository import UserRepository
from app.services.auth_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


# Helper functions to inject the repository and service per request
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository=repo)


@router.post("/register", response_model=UserOut)
async def register(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),  # Injected here
):
    try:
        result = await user_service.create_user(user)
        return result["user"]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, user_service: UserService = Depends(get_user_service)):
    try:
        result = await user_service.authenticate_user(user.email, user.password)
        return {
            "id": result["user"].id,
            "email": result["user"].email,
            "username": result["user"].username,
            "role": result["user"].role,
            "is_active": result["user"].is_active,
            "access_token": result["access_token"],
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
