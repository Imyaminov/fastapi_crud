from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    username: str

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False


class LoginUserSchema(BaseModel):
    username: str
    password: constr(min_length=8)


class UserResponse(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class FilteredUserResponse(UserBaseSchema):
    id: int


class PostBaseSchema(BaseModel):
    title: str
    content: str
    category: str
    user_id: id

    class Config:
        orm_mode = True


class CreatePostSchema(PostBaseSchema):
    pass


class PostResponse(PostBaseSchema):
    id: id
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime


class UpdatePostSchema(BaseModel):
    title: str
    content: str
    category: str
    user_id: id
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class ListPostResponse(BaseModel):
    success: bool
    posts: List[PostResponse]