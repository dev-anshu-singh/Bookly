from fastapi import FastAPI, status
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from .errors import register_all_error
from .middleware import register_all_middleware

# coroutine that will run throughout the lifespan of the application
@asynccontextmanager
async def life_span(app:FastAPI):
    #run at start of app
    print(f"server is starting...")
    # await init_db()
    # not needed anymore, we will do all the db changes with alembic
    # this coroutine was making a book if didn't exsisted earlier, not needed since we are using albemic now
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

register_all_error(app)

register_all_middleware(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['review'])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])