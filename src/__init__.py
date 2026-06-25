from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db

# coroutine that will run throughout the lifespan of the application
@asynccontextmanager
async def life_span(app:FastAPI):
    #run at start of app
    print(f"server is starting...")
    await init_db()
    yield
    # run at the end
    print(f"server has been stopped")


version = 'v1'

app = FastAPI(
    title='Books API',
    description='A Rest API for book review web service',
    version = version,
    lifespan = life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])

