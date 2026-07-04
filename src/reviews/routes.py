from fastapi import APIRouter, Depends
from .service import ReviewService
from src.db.models import User
from src.auth.dependencies import get_current_user, RoleChecker
from src.db.main import get_session
from .schemas import ReviewCreateModel, ReviewModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import RoleChecker

review_router = APIRouter()

review_service = ReviewService()

admin_role_checker = RoleChecker(['admin'])
user_role_checker  = RoleChecker(['user','admin'])

@review_router.post('/book/{book_uid}',response_model=ReviewModel,dependencies=[Depends(user_role_checker)])
async def add_review_to_book(
        book_uid:str,
        review_data:ReviewCreateModel,
        current_user:User=Depends(get_current_user),
        session:AsyncSession = Depends(get_session)
):
    new_review = await review_service.add_review_to_book(
        user_email = current_user.email,
        review_data = review_data,
        book_uid = book_uid,
        session=session
    )
    return new_review

@review_router.get('/',dependencies=[Depends(admin_role_checker)])
async def get_all_reviews(session: AsyncSession = Depends(get_session)):
    reviews_list = await review_service.get_all_reviews(session)
    return reviews_list

@review_router.get('/{review_uid}',dependencies=[Depends(admin_role_checker)])
async def get_review(review_uid:str,session: AsyncSession = Depends(get_session)):
    review = await review_service.get_review(review_uid=review_uid,session=session)
    return review

@review_router.delete('/{review_uid}',dependencies=[Depends(user_role_checker)])
async def delete_review(review_uid:str,session:AsyncSession=Depends(get_session),curr_user:User=Depends(get_current_user)):
    await review_service.delete_review_to_from_book(review_uid=review_uid,user_email=curr_user.email,session=session)
    return None