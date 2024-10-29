from fastapi import FastAPI
import uvicorn
from app.users.router import router as router_users
from app.calls.router import router as router_calls
from app.locations.router import router as router_locations
from app.patients.router import router as router_patients
from app.utils.logger_config import get_logger

app = FastAPI()
app.include_router(router_calls)

app.include_router(router_patients)

app.include_router(router_locations)

app.include_router(router_users)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_config=None)


# @app.exception_handler(TokenExpiredException)
# async def token_expired_exception_handler(request: Request, exc: TokenExpiredException):
#     # Перенаправляем пользователя на страницу /auth
#     return RedirectResponse(url="/auth")
#
# @app.exception_handler(TokenNotFoundException)
# async def token_not_found_exception_handler(request: Request, exc: TokenNotFoundException):
#     # Перенаправляем пользователя на страницу /auth
#     return RedirectResponse(url="/auth")
