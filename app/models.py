from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from .database import Base

movie_genre = Table(
    "movie_genre", Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True)
)

movie_actor = Table(
    "movie_actor", Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", ForeignKey("actors.id"), primary_key=True)
)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    release_year = Column(Integer)
    director_id = Column(Integer, ForeignKey("directors.id"))
    rating = Column(Float, nullable=True)      
    review = Column(String, nullable=True)  

    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    actors = relationship("Actor", secondary=movie_actor, back_populates="movies")
    director = relationship("Director", back_populates="movies")

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")

class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    movies = relationship("Movie", secondary=movie_actor, back_populates="actors")

class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    movies = relationship("Movie", back_populates="director")

