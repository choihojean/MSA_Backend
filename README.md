# MSA_Backend
 MSA 풀스택 개발 파이썬 백엔드
----------------------------------
비동기 프로그래밍(FastAPI + Kafka/RabbitMQ)<br/>
컨테이너 기반 배포(Docker 및 Kubernetes)<br/>
OAuth 2.0 로그인 & JWT 인증<br/>
CI/CD 파이프라인 구축<br/>
Redis 캐싱 & 성능 최적화<br/>


MYSQL 컨테이너로 실행<br/><br/>
로그아웃 시 토큰을 Redis에 저장하는 블랙리스트 방식 사용(해당 JWT로 API 요청 시 401반환하고, 만료 시 redis에서 제거)<br/><br/>
회원탈퇴 시 소프트 삭제 방식(is_deleted=True) 적용<br/><br/>
