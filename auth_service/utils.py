import bcrypt
import jwt
import datetime
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

JWT_SECRET = os.getenv("JWT_SECRET", "default_secret")
JWT_ALGORITHM = "HS256"

#비밀번호 해싱(저장 시)
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw.decode('utf-8')

#비밀번호 검증(db에 저장된 해시와 일치하는지 확인)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


#JWT 토큰 생성
def create_access_token(user_id: int, email: str, expires_delta: int = 60):
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expires_delta)
    payload = {
        "sub":email,
        "user_id":user_id,
        "exp":expire
    }
    return jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)

#JWT 토큰 검증
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None #만료
    except jwt.InvalidTokenError:
        return None #유효하지 않음
