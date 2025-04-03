from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from common.constants import MAX_EMAIL_LENGTH, MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH


class RegisterSchema(BaseModel):
    email: EmailStr = Field(max_length=MAX_EMAIL_LENGTH)
    password: str = Field(
        max_length=MAX_PASSWORD_LENGTH, min_length=MIN_PASSWORD_LENGTH
    )


class JWTTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
