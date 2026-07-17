from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.deps import get_current_user, require_role
from app.models.user import User, UserRole
from app.repositories.post_repository import PostRepository
from app.services.post_service import PostService
from app.schemas.post_schema import (
    PostCreate, PostUpdate, PostReviewAction,
    PostPublicOut, PostAdminOut,
)

router = APIRouter(prefix="/posts", tags=["posts"])


def get_post_service(db: AsyncSession = Depends(get_db)) -> PostService:
    return PostService(repo=PostRepository(db), db=db)


@router.post("/", response_model=PostAdminOut)
async def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service),
):
    return await service.create_post(data, current_user.id)


@router.patch("/{post_id}", response_model=PostAdminOut)
async def update_post(
    post_id: int,
    data: PostUpdate,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service),
):
    try:
        return await service.update_post(post_id, data, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{post_id}/submit", response_model=PostAdminOut)
async def submit_for_review(
    post_id: int,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service),
):
    try:
        return await service.submit_for_review(post_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{post_id}/review", response_model=PostAdminOut)
async def review_post(
    post_id: int,
    action: PostReviewAction,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    service: PostService = Depends(get_post_service),
):
    try:
        return await service.review_post(post_id, action)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/pending", response_model=list[PostAdminOut])
async def list_pending(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    service: PostService = Depends(get_post_service),
):
    return await service.repo.list_pending()


@router.get("/mine", response_model=list[PostAdminOut])
async def list_my_posts(
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service),
):
    return await service.repo.list_by_author(current_user.id)


@router.get("/", response_model=list[PostPublicOut])
async def list_published(service: PostService = Depends(get_post_service)):
    return await service.repo.list_published()


@router.get("/{slug}", response_model=PostPublicOut)
async def get_published_post(slug: str, service: PostService = Depends(get_post_service)):
    post = await service.repo.get_by_slug(slug)
    if post is None or post.status != post.status.PUBLISHED:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    service: PostService = Depends(get_post_service),
):
    try:
        await service.delete_post(post_id, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))