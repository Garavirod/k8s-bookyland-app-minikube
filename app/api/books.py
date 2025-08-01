from pydantic import BaseModel
from fastapi import Depends, HTTPException
from models.books import Book, PyObjectId
from fastapi import APIRouter
from database.db import get_database
from bson import ObjectId
from typing import List

router = APIRouter(prefix='/books')

class BookRequest(BaseModel):
    title: str
    isbn: str
    author_id: str
    genre_id: str

class BookResponse(BaseModel):
    id: str
    title: str
    isbn: str
    author_id: str
    genre_id: str

@router.post('/create-book/', response_model=BookResponse)
async def create_book(item: BookRequest):
    db = get_database()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    # Validate ObjectIds
    try:
        author_id = ObjectId(item.author_id)
        genre_id = ObjectId(item.genre_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid author_id or genre_id")
    
    book_data = {
        "title": item.title,
        "isbn": item.isbn,
        "author_id": author_id,
        "genre_id": genre_id
    }
    
    result = await db.books.insert_one(book_data)
    book_data["_id"] = result.inserted_id
    
    return BookResponse(
        id=str(book_data["_id"]),
        title=book_data["title"],
        isbn=book_data["isbn"],
        author_id=str(book_data["author_id"]),
        genre_id=str(book_data["genre_id"])
    )

@router.get('/books/', response_model=List[BookResponse])
async def get_books():
    db = get_database()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    books = []
    cursor = db.books.find()
    async for document in cursor:
        books.append(BookResponse(
            id=str(document["_id"]),
            title=document["title"],
            isbn=document["isbn"],
            author_id=str(document["author_id"]),
            genre_id=str(document["genre_id"])
        ))
    
    return books
