from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends, Security

from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.logger import logger
from app.roles.service import RoleService
from app.users.auth import create_access_token, get_password_hash, role_required, verify_password
from app.users.schemas import SToken, SUserAuth, SUserCreate
from app.users.service import UserService

router = APIRouter(prefix='/users', tags=['Work with users'])


@router.post('/token', response_model=SToken, description="Get access token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> SToken:
    user = await UserService.find_full_user_data_or_none(username=form_data.username)
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    role = user['role']
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, user_role=role, expires_delta=access_token_expires
    )
    return SToken(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=SUserAuth, description="Register new user")
async def register_user(
        user_data: SUserCreate = Depends(),
        security_scopes=Security(role_required, scopes=['admin']),
) -> SUserAuth:
    logger.info("Calling register_user")
    user = await UserService.find_one_or_none(username=user_data.username)
    logger.debug(f"User: {user}")
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    role = await RoleService.find_one_or_none(name=user_data.role)
    logger.debug(f"Role: {role}")
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Available roles: admin, doctor, driver, operator"
        )

    hashed_password = get_password_hash(user_data.password)

    new_user_data = {
        "username": user_data.username,
        "hashed_password": hashed_password,
        "role_id": role.id,
        "is_active": True
    }
    logger.debug(f"New user data: {new_user_data}")
    new_user = await UserService.add(**new_user_data)

    return SUserAuth(username=new_user.username, is_active=new_user.is_active, role=role.name)


@router.get('/all', response_model=list[SUserAuth], description="Get all users")
async def get_all_users(security_scopes=Security(role_required, scopes=['admin'])) -> list[SUserAuth]:
    users = await UserService.find_all()
    return [SUserAuth.from_orm()]
    return [SUserAuth(username=user['username'], is_active=user['is_active'], role=user['role']) for user in users]
