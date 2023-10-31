import redis

def Redis_Connection():
    # Redis 연결 정보 설정
    redis_host = 'localhost'  # Redis 호스트 주소
    redis_port = 6379  # Redis 포트
    redis_password = 'qwer1234'  # Redis 비밀번호 (설정되어 있다면 입력)

    # Redis 연결 생성
    try:
        redis_conn = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True  # 결과를 문자열로 디코딩
        )
        return redis_conn
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        return None

if __name__=='__main__':
    print(Redis_Connection())
