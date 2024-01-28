import jwt
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Password hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Secret key for JWT
SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'


# Sample User Model
class User(BaseModel):
    username: str
    password: str


# Sample User Data (Replace with database)
fake_users_db = {
    'user1': {
        'username': 'user1',
        'hashed_password': 'hashed_password1'
    }
}


# Verify password
def verify_password(plain_password, hashed_password):
    # ret = pwd_context.verify(plain_password, hashed_password)
    return True


# Authenticate user
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return user


# Create token
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency for token verification
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail='Invalid credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

router = APIRouter(prefix='/token')


@router.post('/', response_description='login for access token')
async def login(user: User):
    user_data = authenticate_user(user.username, user.password)
    if not user_data:
        raise HTTPException(
            status_code=401,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    token = create_access_token(data={'sub': user_data['username']})
    return {'access_token': token, 'token_type': 'bearer'}
