from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.repositories.auth_repository import UserRepository

# tokenUrl points at your login route -- used for FastAPI's auto-generated
# docs/Swagger "Authorize" button, not for actual token validation logic.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 1. Define a reusable HTTPException for "invalid credentials" (401)
    #    you'll raise this from multiple points below

    # 2. Call decode_access_token(token) -- what happens if it returns None?
    #    (hint: raise your 401 here)

    # 3. Pull the email out of the payload's "sub" claim
    #    what if "sub" is missing from the payload? raise 401 again

    # 4. Use UserRepository(db) to look up the user by that email
    #    what if no user is found? raise 401 again

    # 5. Return the user object
    
    # Decode the token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Extract user email from payload
    user_email: str = payload.get("sub")
    if user_email is None:
        raise credentials_exception

    # Fetch user from database
    user = await UserRepository(db).get_user_by_email(user_email)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    return user




def require_role(*allowed_roles: UserRole):
    """Returns a dependency that only allows users with one of the given roles."""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        # if current_user.role not in allowed_roles: raise 403 (not 401 --
        # think about why these are different status codes)
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker