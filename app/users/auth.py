from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt
from jwt import InvalidTokenError

from passlib.context import CryptContext

from app.config import settings
from app.users.service import find_user_by_name


class LoggingOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request):
        token = await super().__call__(request)
        return token


oauth2_scheme = LoggingOAuth2PasswordBearer(
    tokenUrl="users/token/",
    scopes={
        "admin": "Admin access",
        "doctor": "Doctor access",
        "driver": "Driver access",
        "operator": "Operator access",
    },
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    user_role: str = None,
    expires_delta: timedelta | None = None,
):
    to_encode = data.copy()
    scopes = [user_role]
    to_encode.update({"scopes": scopes})
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def validate_token_and_return_scopes(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        scopes = payload.get("scopes", [])
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await find_user_by_name(username=username)
    if user is None:
        raise credentials_exception
    return scopes


async def role_required(
    security_scopes: SecurityScopes,
    token_data: tuple = Depends(validate_token_and_return_scopes),
):
    scopes = token_data

    token_scopes = set(scopes)

    if not token_scopes.intersection(security_scopes.scopes):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
