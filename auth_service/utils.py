import bcrypt

#비밀번호 해싱(저장 시)
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw.decode('utf-8')

#비밀번호 검증(db에 저장된 해시와 일치하는지 확인)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
