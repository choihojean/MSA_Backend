from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .utils import verify_access_token
from .redis_client import is_blacklisted
from .models import User, UserType
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login", auto_error=False) #authorization 헤더에서 Bearer 토큰 자동으로 가져오기

#JWT검증
def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="인증 토큰이 없습니다.",
            headers={"WWW-Authenticate":"Bearer"},
        )
    
    #블랙리스트 체크
    if is_blacklisted(token):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="이미 로그아웃된 토큰입니다.",
            headers={"WWW-Authenticate":"Bearer"},
        )

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, #없거나 만료 시 401 반환
            detail="없거나 만료된 토큰입니다.",
            headers={"WWW-Authenticate":"Bearer"},
        )
    
    return payload
    
#관리자 인증 미들웨어
def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="없거나 만료된 토큰입니다")
    
    db_user = db.query(User).filter(User.id == payload["user_id"]).first()

    if not db_user or db_user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="유저가 아니거나 탈퇴되었습니다.")
    
    if db_user.usertype != UserType.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자 권한이 없습니다.")
    
    return db_user