# 🎬 Movie Explorer Platform

A fully functional **FastAPI** backend to explore, manage, and filter Movies, Genres, Directors, and Actors — with database integration, Swagger docs, unit tests, and linting using **Ruff**.

---

## ✅ Features

- 🚀 CRUD APIs for:
  - 🎞️ Movies
  - 🎭 Actors
  - 🎬 Directors
  - 🏷️ Genres
- 🔄 Relationships:
  - Movies → many Actors
  - Movies → many Genres
  - Movies → one Director
- 🧠 Filters:
  - 🎥 Movies by Genre, Actor, Director, Year
  - 👤 Actors by Genre or Movie
- ⭐ Ratings and Reviews for Movies
- 🧪 Unit tested with **Pytest**
- 🧹 Code linted using **Ruff**
- 📘 OpenAPI docs available at `/docs`
- 🌐 CORS enabled (frontend-ready)
- 🔐 `.env` support for DB credentials

---
## 🚦 Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/movie-explorer-platform.git
    cd movie-explorer-platform
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure environment variables:**
    - Copy `.env.example` to `.env` and update database credentials.

4. **Run database migrations:**
    ```bash
    alembic upgrade head
    ```

5. **Start the FastAPI server:**
    ```bash
    uvicorn app.main:app --reload
    ```

6. **Access API docs:**
    - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

```
## 🧱 Project Structure
ovie-explorer-api/
├── app/                         # 🧠 Core app logic lives here
│   ├── __init__.py              # 📦 Makes 'app' a package
│   ├── database.py              # 🗄️ Database connection config
│   ├── main.py                  # 🚀 FastAPI app and route definitions
│   ├── models.py                # 🧱 SQLAlchemy models
│   └── schemas.py               # 📦 Pydantic request/response models
│
├── tests/                       # 🧪 Unit tests
│   └── test_movies.py           # 🧪 Test cases for routes
│
├── .env                         # 🤫 Secret environment variables
├── .gitignore                   # 🙈 Keeps secrets and clutter out of Git
├── pytest.ini                   # ⚙️ Pytest configuration
├── requirement.txt              # 📦 Python dependencies
└── README.md                    # 📖 You’re looking at it!

```

### 😂 Developer Mood While Debugging

![Debugging Meme](https://i.imgur.com/0y8Ftya.jpeg)

### 🧙‍♂️ Magic Behind the Code