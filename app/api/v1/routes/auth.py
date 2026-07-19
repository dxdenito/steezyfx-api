from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth_schema import UserCreate, UserLogin, UserOut, TokenResponse
from app.schemas.profile_schema import ProfileUpdate, ProfileOut
from app.core.database import get_db

from app.api.v1.deps import get_current_user
from app.repositories.auth_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository
from app.services.auth_service import UserService
from app.services.profile_service import ProfileService

from app.models.user import User, UserRole

router = APIRouter(prefix="/auth", tags=["auth"])


# Helper functions to inject the repository and service per request
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


def get_profile_repository(db: Session = Depends(get_db)) -> ProfileRepository:
    return ProfileRepository(db=db)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository=repo)


def get_profile_service(repo: ProfileRepository = Depends(get_profile_repository)) -> ProfileService:
    return ProfileService(repo=repo)

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
            "profile": result["user"].profile,
            "access_token": result["access_token"],
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.patch("/profile/me", response_model=ProfileOut)
async def upsert_profile(
    data: ProfileUpdate,
    service: ProfileService = Depends(get_profile_service),
    current_user=Depends(get_current_user),
): 
    try:
        return await service.upsert_profile(data,current_user.id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

