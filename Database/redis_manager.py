import os
from dotenv import load_dotenv

load_dotenv()

import redis

def Redis_Connection():
    # Redis 연결 정보 설정
    REDIS_HOST = os.getenv('REDIS_HOST')  # Redis 호스트 주소
    REDIS_PORT = os.getenv('REDIS_PORT')  # Redis 포트

    # Redis 연결 생성
    try:
        redis_conn = redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True  # 결과를 문자열로 디코딩
        )
        return redis_conn
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        return None

if __name__=='__main__':
    print(os.getenv('REDIS_HOST'))
    print(Redis_Connection())
