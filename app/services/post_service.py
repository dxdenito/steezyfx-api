import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.post import Post, PostStatus
from app.models.tag import Tag
from app.models.user import User, UserRole
from app.repositories.post_repository import PostRepository
from app.schemas.post_schema import PostCreate, PostUpdate, PostReviewAction
from app.core.utils import slugify


class PostService:
    def __init__(self, repo: PostRepository, db: AsyncSession):
        self.repo = repo
        self.db = db

    async def _resolve_tags(self, tag_ids: list[int] | None) -> list[Tag]:
        if not tag_ids:
            return []
        result = await self.db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
        return list(result.scalars().all())

    async def _unique_slug(self, base_slug: str) -> str:
        slug = base_slug
        counter = 1
        while await self.repo.get_by_slug(slug) is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    async def create_post(self, data: PostCreate, author_id: int) -> Post:
        base_slug = slugify(data.title)
        slug = await self._unique_slug(base_slug)
        tags = await self._resolve_tags(data.tag_ids)

        post = Post(
            title=data.title,
            slug=slug,
            content=data.content,
            excerpt=data.excerpt,
            category_id=data.category_id,
            tags=tags,
            author_id=author_id,
            status=PostStatus.DRAFT,
        )
        return await self.repo.create(post)

    async def update_post(
        self, post_id: int, data: PostUpdate, current_user: User
    ) -> Post:
        post = await self.repo.get_by_id(post_id)
        if post is None:
            raise ValueError("Post not found")
        if post.author_id != current_user.id:
            raise PermissionError("You can only edit your own posts")
        if post.status not in (PostStatus.DRAFT, PostStatus.REJECTED):
            raise ValueError("Only draft or rejected posts can be edited")

        if data.title is not None:
            post.title = data.title
            post.slug = await self._unique_slug(slugify(data.title))
        if data.content is not None:
            post.content = data.content
        if data.excerpt is not None:
            post.excerpt = data.excerpt
        if data.category_id is not None:
            post.category_id = data.category_id
        if data.tag_ids is not None:
            post.tags = await self._resolve_tags(data.tag_ids)

        return await self.repo.update(post)

    async def submit_for_review(self, post_id: int, current_user: User) -> Post:
        post = await self.repo.get_by_id(post_id)
        if post is None:
            raise ValueError("Post not found")
        if post.author_id != current_user.id:
            raise PermissionError("You can only submit your own posts")
        if post.status not in (PostStatus.DRAFT, PostStatus.REJECTED):
            raise ValueError("Only draft or rejected posts can be submitted")

        post.status = PostStatus.PENDING
        post.rejection_reason = None
        return await self.repo.update(post)

    async def review_post(self, post_id: int, action: PostReviewAction) -> Post:
        post = await self.repo.get_by_id(post_id)
        if post is None:
            raise ValueError("Post not found")
        if post.status != PostStatus.PENDING:
            raise ValueError("Only pending posts can be reviewed")

        if action.action == "approve":
            post.status = PostStatus.PUBLISHED
            post.rejection_reason = None
            from datetime import datetime, timezone

            post.published_at = datetime.now(timezone.utc)
        else:
            post.status = PostStatus.REJECTED
            post.rejection_reason = action.rejection_reason

        return await self.repo.update(post)

    async def delete_post(self, post_id: int, current_user: User) -> None:
        post = await self.repo.get_by_id(post_id)
        if post is None:
            raise ValueError("Post not found")
        if post.author_id != current_user.id and current_user.role != UserRole.ADMIN:
            raise PermissionError("You can only delete your own posts")
        await self.repo.delete(post)
