from typing import List
from src.books.schemas import BookUpdateModel, Book
from fastapi import APIRouter, HTTPException, status, Depends
from src.db.main import get_session
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession

book_router = APIRouter()
book_service = BookService()

@book_router.get('/',response_model=List[Book])
async def get_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books

# /books included as prefix in app

@book_router.post('/',status_code = status.HTTP_201_CREATED, response_model=Book)
async def create_a_books(book_data:Book,session: AsyncSession = Depends(get_session))->dict:
    new_book = await book_service.create_book(book_data,session)
    return new_book

@book_router.get('/{book_uid}',response_model=Book)
async def get_books(book_uid:int,session: AsyncSession = Depends(get_session))->dict:
    book =await book_service.get_book(book_uid,session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch('/{book_uid}')
async def update_books(book_uid:int, book_update_data: BookUpdateModel,session: AsyncSession = Depends(get_session))->dict:
    updated_book = await book_service.update_book(book_uid,book_update_data,session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete('/{book_uid}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_books(book_uid:int,session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid,session)
    if book_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# do not return anything