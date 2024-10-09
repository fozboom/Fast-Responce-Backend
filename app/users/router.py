from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.config import settings
from app.users.auth import create_access_token, get_current_active_user, get_password_hash
from app.users.service import UserService
from app.users.models import User
from app.users.schemas import SToken, SUserAuth, SUserCreate

router = APIRouter(prefix='/users', tags=['Work with users'])
auth = APIRouter()

@router.post('/token', response_model=SToken, description="Get access token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> SToken:
    user = await UserService.find_one_or_none(username=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return SToken(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=SUserAuth)
async def register_user(user_data: SUserCreate = Depends()) -> SUserAuth:
    user = await UserService.find_one_or_none(username=user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = user_data.model_dump()
    new_user.pop("password")
    new_user["hashed_password"] = hashed_password
    await UserService.add(**new_user)

    return SUserAuth(username=new_user['username'], is_active=True)


@router.get("/me", response_model=SUserAuth)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> SUserAuth:
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: Annotated[SUserAuth, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]
