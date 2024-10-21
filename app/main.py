from fastapi import FastAPI

from app.users.router import router as router_users
from app.calls.router import router as router_calls
from app.locations.router import router as router_locations
from app.patients.router import router as router_patients
app = FastAPI()
app.include_router(router_calls)

app.include_router(router_patients)

app.include_router(router_locations)

app.include_router(router_users)




# @app.exception_handler(TokenExpiredException)
# async def token_expired_exception_handler(request: Request, exc: TokenExpiredException):
#     # Перенаправляем пользователя на страницу /auth
#     return RedirectResponse(url="/auth")
#
# @app.exception_handler(TokenNotFoundException)
# async def token_not_found_exception_handler(request: Request, exc: TokenNotFoundException):
#     # Перенаправляем пользователя на страницу /auth
#     return RedirectResponse(url="/auth")
