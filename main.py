import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,status
import models, schemas, crud
from database import engine, SessionLocal
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
import os

models.Base.metadata.create_all(bind=engine)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

class Settings(BaseModel):
    authjwt_secret_key:str= os.environ.get('authjwt_secret_key')


@AuthJWT.load_config
def get_config():
    return Settings()

# Dependency


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/user", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.post("/authenticate", response_model=schemas.Token)
def authenticate_user(user: schemas.UserAuthenticate, db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")
    else:
        is_password_correct = crud.check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password is not correct")
        else:
            access_token=Authorize.create_access_token(subject=user.username)
            # refresh_token=Authorize.create_refresh_token(subject=user.username)
            return {"access_token": access_token, "token_type": "Bearer"}

@app.post("/wedding", response_model=schemas.Token)
def add_wedding_info(wedding: schemas.Wedding, db: Session = Depends(get_db)):
    return crud.add_wedding_info(db, wedding=wedding)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)
