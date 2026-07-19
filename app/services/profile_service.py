from app.schemas.profile_schema import ProfileUpdate
from app.repositories.profile_repository import ProfileRepository
from app.models.profile import Profile


class ProfileService:
    def __init__(self, repo: ProfileRepository):
        self.repo = repo

    async def upsert_profile(self, data: ProfileUpdate, user_id: int) -> Profile:
        user_profile = await self.repo.get_by_user_id(user_id)

        if user_profile is None:
            profile = Profile(
                user_id=user_id,
                bio=data.bio,
                avatar_url=data.avatar_url,
                experience_level=data.experience_level,
            )
            return await self.repo.create_profile(profile)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user_profile, field, value)

        return await self.repo.update_profile(user_profile)
