from sqlalchemy.orm import Session
from . import models
import schemas
from fastapi import HTTPException


# ユーザー一覧取得
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# ルーム一覧取得
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()


# 予約一覧取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


# ユーザー登録
def create_user(db: Session, user: schemas.User):
    db_user = models.User(user_name=user.user_name)
    db.add(db_user)
    # commit()を呼び出すことで、データベースに変更を反映する
    db.commit()
    # refresh()を呼び出すことで、データベースから最新の情報を取得する(例えば自動生成されるuser_idが反映される)
    db.refresh(db_user)
    return db_user


# ルーム登録
def create_room(db: Session, room: schemas.Room):
    db_room = models.Room(
        room_name=room.room_name,
        capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


# 予約登録
def create_booking(db: Session, booking: schemas.Booking):
    db_booked = db.query(models.Booking).\
        filter(models.Booking.room_id == booking.room_id).\
        filter(models.Booking.end_datetime > booking.start_datetime).\
        filter(models.Booking.start_datetime < booking.end_datetime).\
        all()

    if len(db_booked) > 0:
        raise HTTPException(status_code=400, detail="already booked")

    db_booking = models.Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        booked_num=booking.booked_num,
        start_datetime=booking.start_datetime,
        end_datetime=booking.end_datetime)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking