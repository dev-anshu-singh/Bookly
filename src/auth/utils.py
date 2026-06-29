import bcrypt
from datetime import timedelta, datetime
import jwt
from src.config import Config
import uuid
import logging

ACCESS_TOKEN_EXPIRATION = 3600

def generate_password_hash(password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Return as a string to be stored in the database models
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Check the provided password against the hashed version
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def create_access_token(user_data: dict, expiry: timedelta=None, refresh:bool=False):
    payload = {}
    payload['user']=user_data
    payload['exp'] = datetime.now() + (expiry if expiry else timedelta(seconds = ACCESS_TOKEN_EXPIRATION))
    payload['jti']=str(uuid.uuid4())
    # convert to string since we need to serialize it ot json
    payload['refresh']=refresh
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return token

def decode_token(token:str)->dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithm=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None