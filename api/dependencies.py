from fastapi import HTTPException, Request, status

from api.jwt_helper import JWTHelper
from logger import log_func_async


@log_func_async
async def get_user(request: Request):
    authorization = request.headers.get('Authorization')
    user_id = JWTHelper().jwt_authorizer(authorization)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized")
    return int(user_id)
