from fastapi import FastAPI

from app.users.router import router as router_users
from app.roles.router import router as router_roles
from app.calls.router import router as router_calls
from app.statuses.router import router as router_statuses
from app.locations.router import router as router_locations
from app.priority.router import router as router_priority
from app.logger import logger
app = FastAPI()
logger.info("App started")

app.include_router(router_priority)
app.include_router(router_users)
app.include_router(router_roles)
app.include_router(router_statuses)

app.include_router(router_calls)

app.include_router(router_locations)



# @app.exception_handler(TokenExpiredException)
# async def token_expired_exception_handler(request: Request, exc: TokenExpiredException):
#     # Перенаправляем пользователя на страницу /auth
#     return RedirectResponse(url="/auth")
#
# @app.exception_handler(TokenNotFoundException)
# async def token_not_found_exception_handler(request: Request, exc: TokenNotFoundException):
#     # Перенаправляем пользователя на страницу /auth
#     return RedirectResponse(url="/auth")
