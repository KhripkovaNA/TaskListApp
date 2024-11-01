from fastapi import APIRouter, Response, Request
from app.auth.auth import delete_refresh_token
from app.auth.service import register, login, refresh
from app.auth.schemas import SUserRegister, SUserAuth, SAuthRefresh

router = APIRouter(prefix='/auth', tags=['Аутентификация'])


@router.post("/register/", summary="Регистрация нового пользователя")
async def register_user(user_data: SUserRegister) -> dict:
    await register(user_data)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/", summary="Вход в систему")
async def auth_user(response: Response, request: Request, user_data: SUserAuth):
    access_token, refresh_token = await login(user_data, request)
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': refresh_token, 'message': 'Авторизация успешна!'}


@router.post("/refresh/", summary="Обновление access токена")
async def refresh_user(response: Response, request: Request, token_data: SAuthRefresh):
    access_token, refresh_token = await refresh(request, token_data)
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': refresh_token, 'message': 'Авторизация успешна!'}


@router.post("/logout/", summary="Выход из системы")
async def logout_user(response: Response, request: Request, token_data: SAuthRefresh):
    await delete_refresh_token(token_data, request)
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
