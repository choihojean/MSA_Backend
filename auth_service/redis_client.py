import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost") #local을 기본값으로 설정
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


#redis클라이언트 생성
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

#JWT블랙리스트에 추가
def add_to_blacklist(token: str, expires_in: int):
    redis_client.setex(f"blacklist:{token}", expires_in, "blacklisted")

#블랙리스트에 있는지 여부
def is_blacklisted(token: str) -> bool:
    return redis_client.exists(f"blacklist:{token}") > 0