import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from .database import Base

#사용자 유형
class UserType(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, default=False)
    usertype = Column(Enum(UserType), default=UserType.USER)