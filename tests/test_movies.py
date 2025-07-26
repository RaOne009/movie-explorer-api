from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_unique_genre(name="Action"):
    # Check if it already exists
    response = client.get("/genres/")
    existing = [g for g in response.json() if g["name"] == name]
    if existing:
        return existing[0]

    response = client.post("/genres/", json={"name": name})
    assert response.status_code == 200
    return response.json()


def create_unique_actor(name="Arnold Schwarzenegger"):
    # Check if it already exists
    response = client.get("/actors/")
    existing = [a for a in response.json() if a["name"] == name]
    if existing:
        return existing[0]

    response = client.post("/actors/", json={"name": name})
    assert response.status_code == 200
    return response.json()


def create_unique_director(name="James Cameron"):
    response = client.post("/directors/", json={"name": name})
    assert response.status_code == 200
    return response.json()


def create_movie(title="Terminator", year=1984, rating=8.5, review="Classic action"):
    genre = create_unique_genre()
    actor = create_unique_actor()
    director = create_unique_director()

    payload = {
        "title": title,
        "release_year": year,
        "director_id": director["id"],
        "genre_ids": [genre["id"]],
        "actor_ids": [actor["id"]],
        "rating": rating,
        "review": review
    }

    response = client.post("/movies/", json=payload)
    assert response.status_code == 200
    return response.json()


def test_create_genre():
    response = client.post("/genres/", json={"name": "Drama"})
    assert response.status_code == 200
    assert response.json()["name"] == "Drama"


def test_create_actor():
    response = client.post("/actors/", json={"name": "Tom Hanks"})
    assert response.status_code == 200
    assert response.json()["name"] == "Tom Hanks"


def test_create_director():
    response = client.post("/directors/", json={"name": "Christopher Nolan"})
    assert response.status_code == 200
    assert response.json()["name"] == "Christopher Nolan"


def test_create_movie():
    movie = create_movie()
    assert movie["title"] == "Terminator"
    assert movie["release_year"] == 1984
    assert movie["rating"] == 8.5
    assert movie["review"] == "Classic action"


def test_filter_actors_by_genre():
    genre = create_unique_genre("Sci-Fi")
    actor = create_unique_actor("Keanu Reeves")
    director = create_unique_director("Wachowski Sisters")

    payload = {
        "title": "The Matrix",
        "release_year": 1999,
        "director_id": director["id"],
        "genre_ids": [genre["id"]],
        "actor_ids": [actor["id"]],
        "rating": 9.0,
        "review": "Sci-fi classic"
    }
    movie_resp = client.post("/movies/", json=payload)
    assert movie_resp.status_code == 200

    response = client.get(f"/actors/?genre={genre['name']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("Keanu" in a["name"] for a in data)

def test_filter_movies_by_year():
    # First create the movie
    # movie = create_movie(title="Avatar", year=2009, rating=8.0, review="Visually stunning")

    # Then test the filter
    response = client.get("/movies/?year=2009")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(m["title"] == "Avatar" for m in data)



def test_get_all_movies():
    response = client.get("/movies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_actors():
    response = client.get("/actors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_genres():
    response = client.get("/genres/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_directors():
    response = client.get("/directors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
