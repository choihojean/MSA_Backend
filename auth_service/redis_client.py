import redis

#redis클라이언트 생성
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

#JWT블랙리스트에 추가
def add_to_blacklist(token: str, expires_in: int):
    redis_client.setex(f"blacklist:{token}", expires_in, "blacklisted")

#블랙리스트에 있는지 여부
def is_blacklisted(token: str) -> bool:
    return redis_client.exists(f"blacklist:{token}") > 0