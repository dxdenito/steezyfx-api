from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.deps import require_role
from app.models.user import UserRole
from app.repositories.tag_repository import TagRepository
from app.services.tag_service import TagService
from app.schemas.tag_schema import TagCreate, TagUpdate, TagOut

router = APIRouter(prefix="/tags", tags=["tags"])


def get_tag_service(db: AsyncSession = Depends(get_db)) -> TagService:
    return TagService(repo=TagRepository(db))


@router.get("/", response_model=list[TagOut])
async def list_tags(service: TagService = Depends(get_tag_service)):
    return await service.repo.list_all()


@router.post("/", response_model=TagOut)
async def create_tag(
    data: TagCreate,
    current_user=Depends(require_role(UserRole.ADMIN)),
    service: TagService = Depends(get_tag_service),
):
    return await service.create_tag(data)


@router.patch("/{tag_id}", response_model=TagOut)
async def update_tag(
    tag_id: int,
    data: TagUpdate,
    current_user=Depends(require_role(UserRole.ADMIN)),
    service: TagService = Depends(get_tag_service),
):
    try:
        return await service.update_tag(tag_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    current_user=Depends(require_role(UserRole.ADMIN)),
    service: TagService = Depends(get_tag_service),
):
    try:
        await service.delete_tag(tag_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
