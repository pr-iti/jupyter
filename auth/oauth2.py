from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta,timezone
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi import HTTPException, status,Depends
from db import db_user
from dotenv import load_dotenv
import os
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
 
SECRET_KEY = os.getenv("SECRET_KEY") #cmnd to secret key ( openssl rand -hex 32)

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES =os.getenv("ACCESS_TOKEN_EXPIRE")
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def get_current_user(token:str = Depends(oauth2_scheme), db: Session= Depends(get_db)):
  credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details="couldn't  validate credentials",headers={"WWW-Authenticate": "Bearer"}                                      
)
  try:
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  user = db_user.get_user_by_username(db, username)
  
  if user is None:
    raise credentials_exception
  return user
    
  