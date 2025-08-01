from pydantic import BaseModel
from fastapi import Depends, HTTPException
from models.books import Author
from fastapi import APIRouter
from database.db import get_database
from typing import List

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
