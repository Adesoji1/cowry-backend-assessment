from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import requests

from .database import Base, engine, get_db
from .models import Book, User
from .schemas import BookCreate, BookOut, UserCreate, UserOut, UserWithBorrowedBooks
from .config import settings


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Admin Service", version="1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/books", response_model=BookOut)
def add_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Admin can add new books to the catalogue.
    Then notify the frontend service about the new book.
    """
    new_book = Book(
        title=book_data.title,
        publisher=book_data.publisher,
        category=book_data.category,
        is_available=True
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    # Notify the Frontend service
    if settings.FRONTEND_SERVICE_URL:
        try:
            requests.post(f"{settings.FRONTEND_SERVICE_URL}/internal/books", json={
                "id": new_book.id,
                "title": new_book.title,
                "publisher": new_book.publisher,
                "category": new_book.category,
                "is_available": new_book.is_available
            })
        except Exception as e:
            # In real scenario, handle logging/retry
            print(f"Failed to notify Frontend about new book: {e}")

    return new_book

@app.delete("/books/{book_id}")
def remove_book(book_id: int, db: Session = Depends(get_db)):
    """
    Admin can remove a book from the catalogue.
    Then notify the frontend service to remove it.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    # Notify Frontend
    if settings.FRONTEND_SERVICE_URL:
        try:
            requests.delete(f"{settings.FRONTEND_SERVICE_URL}/internal/books/{book_id}")
        except Exception as e:
            print(f"Failed to notify Frontend about book removal: {e}")

    return {"detail": f"Book with id {book_id} removed successfully."}

@app.get("/books/unavailable", response_model=list[BookOut])
def get_unavailable_books(db: Session = Depends(get_db)):
    """
    Fetch/list the books that are not available for borrowing
    (showing the day it will be available).
    """
    books = db.query(Book).filter(Book.is_available == False).all()
    return books


@app.get("/users", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    """
    Fetch / List users enrolled in the library.
    """
    return db.query(User).all()

@app.get("/users/borrowed", response_model=list[UserWithBorrowedBooks])
def get_users_with_borrowed_books(db: Session = Depends(get_db)):
    """
    Fetch / List users and the books they have borrowed
    """
    users = db.query(User).all()
    return users
