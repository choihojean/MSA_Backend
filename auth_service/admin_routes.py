from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .dependencies import get_current_admin
from .models import User, UserType

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

#전체 회원 목록 조회
@admin_router.get("/users")
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    users = db.query(User).all()
    return users

#특정 회원 조회
@admin_router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    return user

@admin_router.post("/users/{user_id}/restore")
def restore_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    user.is_deleted = False
    db.commit()

    return {"message":f"회원 {user_id}의 복구가 성공적으로 완료되었습니다."}

@admin_router.post("/users/{user_id}/promote")
def promote_to_admin(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail = "유저를 찾을 수 없습니다.")
    
    if user.usertype == UserType.ADMIN:
        raise HTTPException(status_code=400, detail = "이미 관리자로 등록된 계정입니다.")
    
    user.usertype = UserType.ADMIN
    db.commit()

    return {"message":f"{user_id}가 관리자로 등록되었습니다."}

#회원 탈퇴(소프트 삭제)
@admin_router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail="유저를 찾을 수 없습니다.")
    
    user.is_deleted = True
    db.commit()
    
    return {"message":f"유저 {user_id}가 성공적으로 탈퇴 되었습니다."}