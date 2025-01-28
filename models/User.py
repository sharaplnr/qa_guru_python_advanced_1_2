from pydantic import BaseModel, EmailStr, HttpUrl, Field


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl

class UserPagination(BaseModel):
    items: list[User] | None = Field(default=[])
    total: int
    page: int
    size: int
    pages: int