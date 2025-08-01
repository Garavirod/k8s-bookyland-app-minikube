from pydantic import BaseModel
from fastapi import Depends, HTTPException
from models.books import Genre
from fastapi import APIRouter
from database.db import get_database
from typing import List

router = APIRouter(prefix='/genres')

class GenreCreate(BaseModel):
    name: str

class GenreResponse(BaseModel):
    id: str
    name: str

@router.post('/create-genre/', response_model=GenreResponse)
async def create_genre(item: GenreCreate):
    db = get_database()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    genre_data = {
        "name": item.name
    }
    
    result = await db.genres.insert_one(genre_data)
    genre_data["_id"] = result.inserted_id
    
    return GenreResponse(
        id=str(genre_data["_id"]),
        name=genre_data["name"]
    )

@router.get('/genres/', response_model=List[GenreResponse])
async def get_genres():
    db = get_database()
    if not db:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    genres = []
    cursor = db.genres.find()
    async for document in cursor:
        genres.append(GenreResponse(
            id=str(document["_id"]),
            name=document["name"]
        ))
    
    return genres

