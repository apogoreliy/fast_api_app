import hashlib
import hmac
from functools import wraps

from fastapi import status

from api.jwt_helper import JWTHelper
from api.controllers.user_controller import UserController

from config import config


def authorize(request):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                authorization = request.headers.get('Authorization')
                user_id = JWTHelper().jwt_authorizer(authorization)
                if not user_id:
                    raise Exception("User is not authorized")

                request.user_id = int(user_id)
                UserController.update_activity(request.user_id)
                return func(*args, **kwargs)
            except Exception as e:
                return {
                    "success": False,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "error_message": str(e),
                }
        return wrapper
    return decorate


def request_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            json_res = res.json()
            print(json_res)
            if json_res.get("status_code") != status.HTTP_200_OK or not json_res.get("success"):
                raise Exception(json_res["error_message"])
            else:
                data = json_res.get("data")
                if data:
                    return data
        except Exception as e:
            print(f"-------------- Error happen: {e}")
    return wrapper


def make_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "error_message": "",
                "data": response,
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error_message": str(e),
                "data": None,
            }

    return wrapper


def make_response_async(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        try:
            response = await f(*args, **kwargs)
            return {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "error_message": "",
                "data": response,
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error_message": str(e),
                "data": None,
            }
    return decorated


def hash_password(password: str) -> str:
    message = password.encode(encoding='UTF-8')
    hmac_sha256 = hmac.new(config["password_key"], msg=message, digestmod=hashlib.sha256)
    password_hash = hmac_sha256.hexdigest()
    return password_hash
