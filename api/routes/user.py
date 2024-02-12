from fastapi import APIRouter, Depends, Query

from typing import Annotated

from api.dependencies import get_user

from api.validation_schemas.user import UserSignupQueryParamsSchema
from api.controllers.user_controller import UserController
from api.utils import hash_password, make_response_async

from messages import messages
from logger import log_func_async

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.put("/signup/", tags=["user"])
@log_func_async
@make_response_async
async def signup(query: UserSignupQueryParamsSchema):
    password_hash = hash_password(query.password)
    user_data = UserController.validate_user_signup_schema(query.email, password_hash)
    is_user_exist = UserController.check_if_user_email_exists(query.email)
    if is_user_exist:
        raise Exception(messages["USER_ALREADY_EXISTS"])

    user_id = UserController.create_new_user(user_data)
    token = UserController.get_jwt_token(user_id)
    return token["access_token"]


@router.get("/login", tags=["user"])
@log_func_async
@make_response_async
async def login(email: Annotated[str, Query(min_length=3, max_length=50)], password: str):
    password_hash = hash_password(password)
    user_id = UserController.get_user_id(email, password_hash)
    if not user_id:
        raise Exception(messages["USER_NOT_FOUND"])

    UserController.update_login_at(user_id)
    token = UserController.get_jwt_token(user_id)
    return token["access_token"]


@router.get("/activity", tags=["user"])
@log_func_async
@make_response_async
async def get_user_activities(user_id: Annotated[int, Depends(get_user)]):
    activities: dict = UserController.get_user_last_login_and_action(user_id)
    return activities
