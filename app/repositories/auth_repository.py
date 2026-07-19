from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.future import select
from app.schemas.auth_schema import UserCreate
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload


class UserRepository:
    # 1. Type hint with AsyncSession instead of Session
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str):

        try:
            # 2. Use select statement and await the database execution
            statement = select(User).options(selectinload(User.profile)).where(User.email == email)
            result = await self.db.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()  # Rollback in case of an error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching user by email: {e}",
            )
            return None

    async def get_user_by_username(self, username: str):

        try:
            # 3. Use select statement and await the database execution
            statement = select(User).options(selectinload(User.profile)).where(User.username == username)
            result = await self.db.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while fetching user by username: {e}",
            )
            return None

    async def create_user(self, user: UserCreate):
        try:
            db_user = User(
                email=user.email, username=user.username, hashed_password=user.password
            )
            self.db.add(db_user)

            # 4. Await commit and refresh for async database calls
            await self.db.commit()
            await self.db.refresh(db_user)
            db_user.profile = None 
            return {"message": "User registered successfully", "user": db_user}
        except SQLAlchemyError as e:
            await self.db.rollback()  # Rollback in case of an error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while creating user: {e}",
            )
            # Rollback if the database transaction fails
            await self.db.rollback()
            return {"error": "Could not register user"}
