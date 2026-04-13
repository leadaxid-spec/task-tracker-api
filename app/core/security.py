from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.user import User
from app.schemas import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None)-> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='not validate')
    if not token:
        raise credentials_exeption
    try:
        payload = jwt.decode(token=token, key = settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        tokendata = TokenPayload(**payload)
        userid = tokendata.sub
        
        if userid is None:
            raise credentials_exeption
    except JWTError:
        raise credentials_exeption
    
    user = await db.execute(select(User).where(User.id == int(userid)))
    user = user.scalar_one_or_none()
    if user is None:
        raise credentials_exeption
    return user
