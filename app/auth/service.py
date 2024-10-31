from app.auth.auth import authenticate_user, create_access_token, create_refresh_token
from app.auth.dao import UsersDAO
from app.auth.exceptions import UserAlreadyExistsException, IncorrectUsernameOrPasswordException
from app.auth.schemas import SUserRegister, SUsername, SUserAdd, SUserAuth


async def register(user_data: SUserRegister):
    user = await UsersDAO.find_one_or_none(filters=SUsername(username=user_data.username))
    if user:
        raise UserAlreadyExistsException
    user_data_dict = user_data.model_dump()
    del user_data_dict['confirm_password']
    await UsersDAO.add(values=SUserAdd(**user_data_dict))


async def login(user_data: SUserAuth) -> tuple:
    user = await authenticate_user(username=user_data.email, password=user_data.password)
    if user is None:
        raise IncorrectUsernameOrPasswordException
    access_token = create_access_token({"sub": str(user.id), "username": user.username})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return access_token, refresh_token
