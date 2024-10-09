from fastapi import FastAPI


from app.users.router import router as router_users
from app.users.router import auth as router_auth
app = FastAPI()

app.include_router(router_users)
app.include_router(router_auth)

# @app.exception_handler(TokenExpiredException)
# async def token_expired_exception_handler(request: Request, exc: TokenExpiredException):
#     # Перенаправляем пользователя на страницу /auth
#     return RedirectResponse(url="/auth")
#
# @app.exception_handler(TokenNotFoundException)
# async def token_not_found_exception_handler(request: Request, exc: TokenNotFoundException):
#     # Перенаправляем пользователя на страницу /auth
#     return RedirectResponse(url="/auth")