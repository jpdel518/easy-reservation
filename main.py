from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import schemas
from sql_app import crud, models
from sql_app.database import SessionLocal, engine

# エンジンを元にデータベースの作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# データベースへのセッションを取得する関数
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    return {"message": "Hello World"}


# User
@app.get("/users", response_model=List[schemas.User])
async def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


# Room
@app.get("/rooms", response_model=List[schemas.Room])
async def fetch_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_rooms(db, skip=skip, limit=limit)


@app.post("/rooms", response_model=schemas.Room)
async def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db=db, room=room)


# Booking
@app.get("/bookings", response_model=List[schemas.Booking])
async def fetch_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bookings(db, skip=skip, limit=limit)


@app.post("/bookings", response_model=schemas.Booking)
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)
