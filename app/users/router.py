from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends, Security

from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.users.auth import create_access_token, get_password_hash, role_required, verify_password
from app.users.schemas import SToken, SUserAuth, SUserCreate
from app.users.service import find_all_users, find_user_by_name, add_user

router = APIRouter(prefix='/users', tags=['Work with users'])


@router.post('/token', response_model=SToken, description="Get access token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> SToken:
    user = await find_user_by_name(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, user_role=user.role, expires_delta=access_token_expires
    )
    refresh_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(days=180))
    # await UserService.save_refresh_token(username=user.username, refresh_token=refresh_token)
    return SToken(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh")
async def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = await find_user_by_name(username=username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        access_token = create_access_token(data={"sub": username}, user_role=user.role)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/register", response_model=SUserAuth, description="Register new user")
async def register_user(
        user_data: SUserCreate = Depends(),
        security_scopes=Security(role_required, scopes=['admin']),
) -> SUserAuth:
    user = await find_user_by_name(username=user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    hashed_password = get_password_hash(user_data.password)

    new_user_data = user_data.model_dump()
    new_user_data['hashed_password'] = hashed_password
    new_user_data.pop('password')
    new_user = await add_user(**new_user_data)

    return SUserAuth.model_validate(new_user)


@router.get('/all', response_model=list[SUserAuth], description="Get all users")
async def get_all_users(security_scopes=Security(role_required, scopes=['admin'])) -> list[SUserAuth]:
    users = await find_all_users()
    return [SUserAuth.model_validate(user) for user in users]
