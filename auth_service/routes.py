from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .utils import hash_password, verify_password, create_access_token
from .schemas import UserCreate, LoginRequest

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

@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    #사용자 존재 확인인
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code = 400, detail="이메일이나 비밀번호가 올바르지 않습니다.")
    
    #비밀번호 검증
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code = 400, detail="이메일이나 비밀번호가 올바르지 않습니다.")
    
    #JWT토큰 생성
    access_token = create_access_token(user_id=db_user.id, email=db_user.email)

    return {"access_token": access_token, "token_type": "bearer"}