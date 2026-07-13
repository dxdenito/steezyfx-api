from app.core.security import hash_password
from app.core.security import verify_password
from app.core.security import create_access_token


class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def get_user_by_email(self, email: str):

        return await self.user_repository.get_user_by_email(email)

    async def get_user_by_username(self, username: str):

        return await self.user_repository.get_user_by_username(username)

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        return verify_password(password, hashed_password)

    async def create_user(self, user_data):

        existing_user_email = await self.get_user_by_email(user_data.email)
        if existing_user_email:
            raise ValueError("User with this email already exists")
        existing_user_username = await self.get_user_by_username(user_data.username)
        if existing_user_username:
            raise ValueError("User with this username already exists")

        user_data.password = hash_password(user_data.password)
        print(user_data.password)
        return await self.user_repository.create_user(user_data)

    async def authenticate_user(self, email: str, password: str):
        user = await self.get_user_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        if not await self.verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        # Create an access token for the authenticated user
        access_token = create_access_token(data={"sub": user.email})
        return {
            "message": "Login successful",
            "user": user,
            "access_token": access_token,
        }
