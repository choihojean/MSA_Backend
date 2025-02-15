import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import User, UserType
from .utils import hash_password, verify_password, create_access_token
from .schemas import UserCreate, LoginRequest, ChangePasswordRequest
from .dependencies import get_current_user, oauth2_scheme
from .redis_client import add_to_blacklist

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        if existing_user.is_deleted:
            existing_user.is_deleted=False
            existing_user.password = hashed_password
            db.commit()
            return {"message":"삭제된 계정을 복구했습니다. 다시 로그인하세요"}
        raise HTTPException(status_code = 400, detail = "이미 등록된 이메일입니다.")

    #비밀번호 암호화
    hashed_password = hash_password(user.password)

    #사용자 생성
    new_user = User(
        email = user.email, 
        password = hashed_password, 
        name = user.name,
        usertype=UserType.USER
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "회원가입이 성공적으로 완료되었습니다.", "user_id": new_user.id} 

@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    #사용자 존재 확인인
    db_user = db.query(User).filter(User.email == user.email, User.is_deleted==False).first()
    if not db_user:
        raise HTTPException(status_code = 400, detail="이메일이나 비밀번호가 올바르지 않습니다.")
    
    #비밀번호 검증
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code = 400, detail="이메일이나 비밀번호가 올바르지 않습니다.")
    
    #JWT토큰 생성
    access_token = create_access_token(user_id=db_user.id, email=db_user.email)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(user: dict = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    expires_in = user["exp"] - int(datetime.datetime.now(datetime.UTC).timestamp())
    if expires_in > 0:
        add_to_blacklist(token, expires_in)

    return {"message": "성공적으로 로그아웃 되었습니다."}

@router.post("/change-password")
def change_password(
    request: ChangePasswordRequest,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    db_user = db.query(User).filter(User.id == user["user_id"],User.is_deleted == False).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="존재하는 유저가 아닙니다.")
    
    #현재 PW확인
    if not verify_password(request.current_password, db_user.password):
        raise HTTPException(status_code = 404, detail="현재 비밀번호가 일치하지 않습니다.")
    
    #새 PW 암호화 후 저장
    db_user.password = hash_password(request.new_password)
    db.commit()

    #모든 세션에서 logout(JWT블랙리스트에 추가가)
    expires_in = user["exp"] - int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    if expires_in > 0:
        add_to_blacklist(token, expires_in)

    return {"message":"비밀번호 변경이 성공적으로 완료되었습니다. 다시 로그인 해주세요."}



@router.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {
        "message": "보호된 엔드포인트입니다",
        "user": user
    }

@router.get("/me")
def get_user_info(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user["user_id"]).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    return {
        "id":db_user.id,
        "email":db_user.email,
        "name":db_user.name
    }

@router.delete("/delete-account")
def delete_account(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    db_user = db.query(User).filter(User.id == user["user_id"]).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    #삭제된 계정인지
    if db_user.is_deleted:
        raise HTTPException(status_code=400, detail="이미 삭제된 계정입니다.")
    
    db_user.is_deleted = True
    db.commit()

    expires_in = user["exp"] - int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    if expires_in > 0:
        add_to_blacklist(token, expires_in)

    return {"message": "계정이 성공적으로 삭제되었습니다."}
    