from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.core.utils import slugify  # move slugify here, shared helper


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def create_category(self, data: CategoryCreate) -> Category:
        slug = slugify(data.name)
        category = Category(name=data.name, slug=slug, description=data.description)
        return await self.repo.create(category)

    async def update_category(self, category_id: int, data: CategoryUpdate) -> Category:
        category = await self.repo.get_by_id(category_id)
        if category is None:
            raise ValueError("Category not found")

        if data.name is not None:
            category.name = data.name
            category.slug = slugify(data.name)
        if data.description is not None:
            category.description = data.description
        if data.is_active is not None:
            category.is_active = data.is_active

        return await self.repo.update(category)

    async def delete_category(self, category_id: int) -> None:
        category = await self.repo.get_by_id(category_id)
        if category is None:
            raise ValueError("Category not found")
        await self.repo.delete(category)