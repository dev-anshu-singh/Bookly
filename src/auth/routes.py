from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserLoginModel, UserModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import verify_password, create_access_token, decode_token
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIERY = 2

@auth_router.post("/signup",
                  response_model=UserModel,
                  status_code=status.HTTP_201_CREATED
                  )
async def create_user_Account(user_data:UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(email,session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User already exists")
    else:
        new_user = await user_service.create_user(user_data,session)

        return new_user


@auth_router.post("/login")
async def login_user(user_login_data: UserLoginModel,session: AsyncSession = Depends(get_session)):
    email = user_login_data.email
    password = user_login_data.password

    user = await user_service.get_user_by_email(email,session)

    if user is not None:
        password_valid = verify_password(password,user.password_hash)
        if password_valid:
            access_token = create_access_token(user_data = {
                'email': user.email,
                'user_uid':str(user.uid)
                }
            )
            refresh_token = create_access_token(user_data = {
                'email':user.email,
                'user_uid':str(user.uid)
            },
            refresh=True,
            expiry=timedelta(days=REFRESH_TOKEN_EXPIERY)
            )
            return JSONResponse(
                content={
                    "message":"Login Successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid":str(user.uid)
                    }
                }
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Email or password invalid"
    )
