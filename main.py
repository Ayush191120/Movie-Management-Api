from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from prisma import Prisma

db = Prisma()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    print("Connected to database")
    yield
    await db.disconnect()
    print("Disconnected from database")

app = FastAPI(title="Movie API", lifespan=lifespan)

@app.post("/movies", status_code=status.HTTP_201_CREATED)
async def create_movie(request: Request):
    try:
        form = await request.form()

        title = form.get("title")
        director = form.get("director")
        release_year = form.get("releaseYear")
        genre = form.get("genre")
        rating = form.get("rating")

        # Validate required fields
        if not title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required title"
            )

        # Create movie in DB
        new_movie = await db.movie.create(
            data={
                "title": title,
                "director": director,
                "releaseYear": release_year,
                "genre": genre,
                "rating": rating,
            }
        )

        print(f"Movie created: {new_movie.title}")

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "id": new_movie.id,
                "title": new_movie.title,
                "message": "Movie created successfully"
            }
        )

    except Exception as e:
        # Unexpected DB or server errors
        print("Error creating movie:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the movie"
        )
    


@app.get("/movies", status_code=status.HTTP_200_OK)
async def get_movies():
    try:
        movies = await db.movie.find_many(order={"createdAt": "desc"})
        
        return {
            "count": len(movies),
            "movies": jsonable_encoder(movies)
        }


    except Exception as e:
        print("Error fetching movies:", e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An error occurred while fetching movies"}
        )
    
@app.get("/movies/{id}", status_code=200)
async def get_movie(id: str):
    try:
        movie = await db.movie.find_unique(where={"id": id})

        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        return jsonable_encoder(movie)

    except Exception as e:
        print("Error fetching movie:", e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching the movie")


@app.put("/movies/{id}", status_code=200)
async def update_movie(
    id: str,
    title: str = Form(None),
    director: str = Form(None),
    releaseYear: int = Form(None),
    genre: str = Form(None),
    rating: int = Form(None),
):
    try:
        # Build dynamic update data
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if director is not None:
            update_data["director"] = director
        if releaseYear is not None:
            update_data["releaseYear"] = releaseYear
        if genre is not None:
            update_data["genre"] = genre
        if rating is not None:
            update_data["rating"] = rating

        if not update_data:
            raise HTTPException(status_code=400, detail="No update fields provided")

        movie = await db.movie.update(
            where={"id": id},
            data=update_data
        )

        return {"message": "Movie updated successfully"}

    except Exception as e:
        print("Error updating movie:", e)
        raise HTTPException(status_code=500, detail="An error occurred while updating the movie")


@app.delete("/movies/{id}", status_code=200)
async def delete_movie(id: str):
    try:
        # First check if movie exists
        movie = await db.movie.find_unique(where={"id": id})
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        # Delete movie
        await db.movie.delete(where={"id": id})

        return {"message": f"Movie with id {id} deleted successfully"}

    except Exception as e:
        print("Error deleting movie:", e)
        raise HTTPException(status_code=500, detail="An error occurred while deleting the movie")