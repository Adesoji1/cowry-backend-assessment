from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


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

class BookFilterQuery(BaseModel):
    publisher: Optional[str] = None
    category: Optional[str] = None

# --- For internal sync from Admin ---
class BookSync(BaseModel):
    id: int
    title: str
    publisher: str
    category: str
    is_available: bool
