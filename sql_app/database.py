from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 格納先のデータベースのパスを指定
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# connect_args={"check_same_thread": False}はSqliteの場合のみ必要
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocalはデータベースへのセッションを表すクラス
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Baseはデータベースのモデルを作成する際に必要な基底クラス
Base = declarative_base()
