from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema, util, oauth2
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schema.Token)
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Implementation for user login,
    db_user = db.query(models.User).filter(models.User.email == user.username).first()
    if not db_user or not util.verify(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = oauth2.create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}