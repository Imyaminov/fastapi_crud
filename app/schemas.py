from pydantic import BaseModel


class PostSchema(BaseModel):
    title: str
    content: str
    category: str
    author_id: int

    class Config:
        orm_mode = True


class AuthorSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True
