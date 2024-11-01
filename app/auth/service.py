from app.auth.auth import authenticate_user, create_access_token, create_refresh_token, validate_refresh_token
from app.auth.dao import UsersDAO
from app.auth.exceptions import UserAlreadyExistsException, IncorrectUsernameOrPasswordException
from app.auth.schemas import SUserRegister, SUsername, SUserAdd, SUserAuth, SAuthRefresh


async def register(user_data: SUserRegister):
    user = await UsersDAO.find_one_or_none(filters=SUsername(username=user_data.username))
    if user:
        raise UserAlreadyExistsException
    await UsersDAO.add(values=SUserAdd(username=user_data.username, password_hash=user_data.password))


async def login(user_data: SUserAuth, request) -> tuple:
    user = await authenticate_user(username=user_data.username, password=user_data.password)
    if user is None:
        raise IncorrectUsernameOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = await create_refresh_token({"sub": str(user.id)}, user_data.fingerprint, request)
    return access_token, refresh_token


async def refresh(request, token_data: SAuthRefresh) -> tuple:
    sub = await validate_refresh_token(token_data, request)
    access_token = create_access_token({"sub": sub})
    refresh_token = await create_refresh_token({"sub": sub}, token_data.fingerprint, request)
    return access_token, refresh_token
