from app.models.tag import Tag
from app.repositories.tag_repository import TagRepository
from app.schemas.tag_schema import TagCreate, TagUpdate
from app.core.utils import slugify  # move slugify here, shared helper


class TagService:
    def __init__(self, repo: TagRepository):
        self.repo = repo

    async def create_tag(self, data: TagCreate) -> Tag:
        slug = slugify(data.name)
        tag = Tag(name=data.name, slug=slug, description=data.description)
        return await self.repo.create(tag)

    async def update_tag(self, tag_id: int, data: TagUpdate) -> Tag:
        tag = await self.repo.get_by_id(tag_id)
        if tag is None:
            raise ValueError("Tag not found")

        if data.name is not None:
            tag.name = data.name
            tag.slug = slugify(data.name)
        if data.description is not None:
            tag.description = data.description
        if data.is_active is not None:
            tag.is_active = data.is_active

        return await self.repo.update(tag)

    async def delete_tag(self, tag_id: int) -> None:
        tag = await self.repo.get_by_id(tag_id)
        if tag is None:
            raise ValueError("Tag not found")
        await self.repo.delete(tag)