from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserPatch(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class AuthorSchema(BaseModel):
    name: str


class AuthorPublic(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class AuthorList(BaseModel):
    authors: list[AuthorSchema]


class BookSchema(BaseModel):
    title: str
    year: int
    author_id: int


class BookPublic(BaseModel):
    id: int
    title: str
    year: int
    author_id: int
    model_config = ConfigDict(from_attributes=True)


class BookPatch(BaseModel):
    title: str | None = None
    year: int | None = None
    author_id: int | None = None


class BookList(BaseModel):
    books: list[BookSchema]
