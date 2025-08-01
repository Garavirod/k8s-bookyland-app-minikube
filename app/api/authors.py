from pydantic import BaseModel
from fastapi import Depends, HTTPException
from models.books import Author
from fastapi import APIRouter
from database.db import get_database
from typing import List
from bson import ObjectId

router = APIRouter(prefix='/authors')

class AuthorRequest(BaseModel):
    name: str
    last_name: str

class AuthorResponse(BaseModel):
    id: str
    name: str
    last_name: str

@router.post('/create-author/', response_model=AuthorResponse)
async def create_author(item: AuthorRequest):
    db = get_database()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    author_data = {
        "name": item.name,
        "last_name": item.last_name
    }
    
    result = await db.authors.insert_one(author_data)
    author_data["_id"] = result.inserted_id
    
    return AuthorResponse(
        id=str(author_data["_id"]),
        name=author_data["name"],
        last_name=author_data["last_name"]
    )

@router.get('/authors/', response_model=List[AuthorResponse])
async def get_authors():
    db = get_database()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    authors = []
    cursor = db.authors.find()
    async for document in cursor:
        authors.append(AuthorResponse(
            id=str(document["_id"]),
            name=document["name"],
            last_name=document["last_name"]
        ))
    
    return authors

@router.delete('/delete-author/{author_id}')
async def delete_author(author_id: str):
    db = get_database()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        author_object_id = ObjectId(author_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid author ID")
    
    # First, check if author exists
    author = await db.authors.find_one({"_id": author_object_id})
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # Delete all books associated with this author (cascade delete)
    books_deleted = await db.books.delete_many({"author_id": author_object_id})
    
    # Delete the author
    result = await db.authors.delete_one({"_id": author_object_id})
    
    return {
        "message": f"Author '{author['name']} {author['last_name']}' deleted successfully",
        "author_deleted": result.deleted_count > 0,
        "books_deleted": books_deleted.deleted_count
    }
