from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .utils import hash_password
from .schemas import UserCreate

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail = "이미 등록된 이메일입니다.")

    #비밀번호 암호화
    hashed_password = hash_password(user.password)

    #사용자 생성
    new_user = User(email = user.email, password = hashed_password, name = user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message:": "회원가입이 성공적으로 완료되었습니다.", "user_id": new_user.id} 