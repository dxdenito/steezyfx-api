from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.models.post import Post, PostStatus
from app.schemas.post_schema import PostCreate, PostUpdate


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, post_id: int) -> Post | None:
        try:
            statement = (
                select(Post)
                .options(
                    selectinload(Post.author),
                    selectinload(Post.tags),
                    selectinload(Post.category),
                )
                .where(Post.id == post_id)
            )
            result = await self.db.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()  # Rollback in case of an error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching post by ID: {e}",
            )

    async def get_by_slug(self, slug: str) -> Post | None:

        try:
            statement = (
                select(Post)
                .options(
                    selectinload(Post.author),
                    selectinload(Post.tags),
                    selectinload(Post.category),
                )
                .where(Post.slug == slug)
            )
            result = await self.db.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching post by slug: {e}",
            )

    async def list_published(self, limit: int = 20, offset: int = 0) -> list[Post]:
        try:
            statement = (
                select(Post)
                .where(Post.status == PostStatus.PUBLISHED)
                .options(
                    selectinload(Post.author),
                    selectinload(Post.tags),
                    selectinload(Post.category),
                )
                .offset(offset)
                .limit(limit)
            )
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching published posts: {e}",
            )

    async def list_by_author(
        self, author_id: int, limit: int = 20, offset: int = 0
    ) -> list[Post]:
        # a user's own dashboard -- ALL their posts regardless of status

        try:
            statement = (
                select(Post)
                .where(Post.author_id == author_id)
                .options(
                    selectinload(Post.author),
                    selectinload(Post.tags),
                    selectinload(Post.category),
                )
                .offset(offset)
                .limit(limit)
            )
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching posts by author: {e}",
            )

    async def list_pending(self, limit: int = 20, offset: int = 0) -> list[Post]:
        # admin's review queue -- status == PENDING only

        try:
            statement = (
                select(Post)
                .where(Post.status == PostStatus.PENDING)
                .options(
                    selectinload(Post.author),
                    selectinload(Post.tags),
                    selectinload(Post.category),
                )
                .offset(offset)
                .limit(limit)
            )
            result = await self.db.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching pending posts: {e}",
            )

    async def create(self, post: Post) -> Post:

        try:
            self.db.add(post)
            await self.db.commit()
            await self.db.refresh(post, attribute_names=["category", "tags"])
            return post
        except SQLAlchemyError as e:
            await self.db.rollback()  # Rollback in case of an error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while creating post: {e}",
            )

    async def update(self, post: Post) -> Post:

        try:
            await self.db.commit()
            await self.db.refresh(post)
            return post
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while updating post: {e}",
            )

    async def delete(self, post: Post) -> None:

        try:
            await self.db.delete(post)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while deleting post: {e}",
            )
