import datetime
from pydantic import BaseModel, Field


# 予約登録時に使うスキーマ（予約作成時にはbooking_idは不要なため）
class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    booked_num: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime


# 予約情報（BookingCraeteを継承している）
class Booking(BookingCreate):
    booking_id: int

    # FastAPIからはdict型で受け取るが、ORM(SQLAlchemy)のモデルが入ってきても大丈夫なようにする
    class Config:
        orm_mode = True


# ユーザー登録時に使うスキーマ（ユーザー作成時にはuser_idは不要なため）
class UserCreate(BaseModel):
    user_name: str = Field(max_length=12)


# ユーザー情報（UserCreateを継承している）
class User(UserCreate):
    user_id: int

    # FastAPIからはdict型で受け取るが、ORM(SQLAlchemy)のモデルが入ってきても大丈夫なようにする
    class Config:
        orm_mode = True


# ルーム登録時に使うスキーマ（ルーム作成時にはroom_idは不要なため）
class RoomCreate(BaseModel):
    room_name: str = Field(max_length=12)
    capacity: int


# ルーム情報（RoomCreateを継承している）
class Room(RoomCreate):
    room_id: int

    # FastAPIからはdict型で受け取るが、ORM(SQLAlchemy)のモデルが入ってきても大丈夫なようにする
    class Config:
        orm_mode = True
