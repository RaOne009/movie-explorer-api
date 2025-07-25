# app/schemas.py

from pydantic import BaseModel
from typing import List, Optional


# ---------- Genre ----------
class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Director ----------
class DirectorBase(BaseModel):
    name: str


class DirectorCreate(DirectorBase):
    pass


class Director(DirectorBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Actor ----------
class ActorBase(BaseModel):
    name: str


class ActorCreate(ActorBase):
    pass


class Actor(ActorBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Movie ----------
class MovieBase(BaseModel):
    title: str
    release_year: int
    director_id: int
    rating: Optional[float] = None
    review: Optional[str] = None


class MovieCreate(MovieBase):
    genre_ids: List[int]
    actor_ids: List[int]


class Movie(MovieBase):
    id: int
    director: Optional[Director]  # Optional here, depending on join
    genres: List[Genre]
    actors: List[Actor]

    class Config:
        from_attributes = True
