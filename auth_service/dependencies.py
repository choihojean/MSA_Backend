from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .utils import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login") #authorization 헤더에서 Bearer 토큰 자동으로 가져오기

#JWT검증
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, #없거나 만료 시 401 반환
            detail="없거나 만료된 토큰입니다",
            headers={"WWW-Authenticate":"Bearer"},
        )
    
    return payload