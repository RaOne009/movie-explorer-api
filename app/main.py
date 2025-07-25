from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
# Initialize the database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Movie Explorer API",
    version="1.0",
    description="A backend API to explore movies, actors, genres, and directors.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a movie with relationships to genres, actors, and a director
@app.post("/movies", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(database.get_db)):
    db_movie = models.Movie(
        title=movie.title,
        release_year=movie.release_year,
        director_id=movie.director_id,
        rating=movie.rating,
        review=movie.review
    )
    db_movie.genres = db.query(models.Genre).filter(models.Genre.id.in_(movie.genre_ids)).all()
    db_movie.actors = db.query(models.Actor).filter(models.Actor.id.in_(movie.actor_ids)).all()
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# List movies with filtering support
@app.get("/movies", response_model=list[schemas.Movie])
def list_movies(
    genre: str = None,
    actor: str = None,
    director: str = None,
    year: int = None,
    db: Session = Depends(database.get_db)):
    query = db.query(models.Movie)
    if genre:
        query = query.join(models.Movie.genres).filter(models.Genre.name == genre)
    if actor:
        query = query.join(models.Movie.actors).filter(models.Actor.name == actor)
    if director:
        query = query.join(models.Movie.director).filter(models.Director.name == director)
    if year:
        query = query.filter(models.Movie.release_year == year)
    return query.all()

# Create and list directors
@app.post("/directors", response_model=schemas.Director)
def create_director(director: schemas.DirectorCreate, db: Session = Depends(database.get_db)):
    db_director = models.Director(name=director.name)
    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director

@app.get("/directors", response_model=list[schemas.Director])
def list_directors(db: Session = Depends(database.get_db)):
    return db.query(models.Director).all()

# Create and list actors, with optional filters by genre or movie
@app.post("/actors", response_model=schemas.Actor)
def create_actor(actor: schemas.ActorCreate, db: Session = Depends(database.get_db)):
    db_actor = models.Actor(name=actor.name)
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor


@app.get("/actors", response_model=list[schemas.Actor])
def list_actors(movie: str = None, genre: str = None, db: Session = Depends(database.get_db)):
    query = db.query(models.Actor)
    if movie:
        query = query.join(models.Actor.movies).filter(models.Movie.title == movie)
    if genre:
        query = query.join(models.Actor.movies).join(models.Movie.genres).filter(models.Genre.name == genre)
    results = query.all()
    if not results:
        return JSONResponse(status_code=200, content=[])
    return results
# Create and list genres
@app.post("/genres/", response_model=schemas.Genre)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(database.get_db)):
    db_genre = models.Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@app.get("/genres/", response_model=list[schemas.Genre])
def list_genres(db: Session = Depends(database.get_db)):
    return db.query(models.Genre).all()

# Get a movie by ID with all relationships
@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int, db: Session = Depends(database.get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie