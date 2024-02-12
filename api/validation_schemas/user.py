from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserSignupSchema(BaseModel):
    email: EmailStr
    password_hash: str
    created_at: datetime | None
    logged_in_at: datetime | None
    last_activity_at: datetime | None


class UserSignupQueryParamsSchema(BaseModel):
    email: EmailStr
    password: str
