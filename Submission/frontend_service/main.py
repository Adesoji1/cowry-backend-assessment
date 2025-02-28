from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .database import Base, engine, get_db
from .models import User, Book
from .schemas import (
    UserCreate, UserOut,
    BookOut, BookFilterQuery, BookSync
)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Frontend Service", version="1.0")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/users", response_model=UserOut)
def enroll_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Enroll users into the library using their email, firstname and lastname.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    new_user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/books", response_model=list[BookOut])
def list_available_books(db: Session = Depends(get_db)):
    """
    List all available books
    """
    books = db.query(Book).filter(Book.is_available == True).all()
    return books

@app.get("/books/{book_id}", response_model=BookOut)
def get_single_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get a single book by its ID
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or not book.is_available:
        raise HTTPException(status_code=404, detail="Book not found or not available.")
    return book

@app.get("/books/filter", response_model=list[BookOut])
def filter_books(publisher: str = None, category: str = None, db: Session = Depends(get_db)):
    """
    Filter books by publisher and/or category
    """
    query = db.query(Book).filter(Book.is_available == True)

    if publisher:
        query = query.filter(Book.publisher.ilike(f"%{publisher}%"))
    if category:
        query = query.filter(Book.category.ilike(f"%{category}%"))

    return query.all()

@app.post("/borrow/{book_id}")
def borrow_book(book_id: int, days: int = Body(..., embed=True), user_id: int = Body(..., embed=True), db: Session = Depends(get_db)):
    """
    Borrow books by id (specify how long you want it for in days).
    In a real scenario, you'd figure out the user from auth or from a parameter.
    """
    book = db.query(Book).filter(Book.id == book_id, Book.is_available == True).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not available or doesn't exist.")

    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    
    book.is_available = False
    book.borrowed_by = user.id
    book.borrowed_until = datetime.utcnow() + timedelta(days=days)

    db.commit()
    db.refresh(book)
    return {"detail": f"Book '{book.title}' borrowed by {user.email} for {days} days."}


@app.post("/internal/books")
def sync_new_book(book_data: BookSync, db: Session = Depends(get_db)):
    """
    This is called by the Admin service to create a new book entry on the frontend side.
    """
    existing_book = db.query(Book).filter(Book.id == book_data.id).first()
    if existing_book:
        # If it already exists, just update
        existing_book.title = book_data.title
        existing_book.publisher = book_data.publisher
        existing_book.category = book_data.category
        existing_book.is_available = book_data.is_available
    else:
        new_book = Book(
            id=book_data.id,
            title=book_data.title,
            publisher=book_data.publisher,
            category=book_data.category,
            is_available=book_data.is_available
        )
        db.add(new_book)
    db.commit()
    return {"detail": "Book synced successfully from Admin."}

@app.delete("/internal/books/{book_id}")
def sync_remove_book(book_id: int, db: Session = Depends(get_db)):
    """
    This is called by the Admin service to remove a book from the frontend side.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return {"detail": "Book removal synced successfully from Admin."}
