from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BookBase(BaseModel):
    title: str
    publisher: str
    category: str

class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    id: int
    is_available: bool
    borrowed_by: Optional[int]
    borrowed_until: Optional[datetime]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True


class UserWithBorrowedBooks(UserOut):
    borrowed_books: List[BookOut] = []
    class Config:
        from_attribute = True
        #orm_mode = True