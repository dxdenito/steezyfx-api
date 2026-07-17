from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.deps import require_role
from app.models.user import UserRole
from app.repositories.category_repository import CategoryRepository
from app.services.category_service import CategoryService
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(repo=CategoryRepository(db))


@router.get("/", response_model=list[CategoryOut])
async def list_categories(service: CategoryService = Depends(get_category_service)):
    return await service.repo.list_all()


@router.post("/", response_model=CategoryOut)
async def create_category(
    data: CategoryCreate,
    current_user=Depends(require_role(UserRole.ADMIN)),
    service: CategoryService = Depends(get_category_service),
):
    return await service.create_category(data)


@router.patch("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    current_user=Depends(require_role(UserRole.ADMIN)),
    service: CategoryService = Depends(get_category_service),
):
    try:
        return await service.update_category(category_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    current_user=Depends(require_role(UserRole.ADMIN)),
    service: CategoryService = Depends(get_category_service),
):
    try:
        await service.delete_category(category_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))