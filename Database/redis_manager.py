import redis
import json
from datetime import datetime

redis_params = {
    'host':'43.201.204.226',
    'port':6379,
    'db':0
}
redis_conn = redis.StrictRedis(
    host=redis_params['host'],
    port=redis_params['port'],
    db=redis_params['db']
    )

def Insert_Job(query: str, activity_type: str, user_id: str):
    try:
        # 현재 시간을 문자열로 변환
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 작업에 추가 정보 포함
        job1 = {
            'query': query,
            'timestamp': current_time,
            'activity_type': activity_type,
            'user_id': user_id,
        }

        json_data = json.dumps(job1)

        # Redis 큐에 작업 추가
        redis_conn.lpush('postgresQueue', json_data)
    except:
        print('error')
        raise Exception("Redis Add Job Failed")

def process_job(job):
    try:
        job_data = json.loads(job)
        query = job_data['query']

        # PostgreSQL에서 쿼리 실행
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()

        # 작업이 성공적으로 처리되었을 경우, 로그 등을 남길 수 있습니다.
        print("Query executed successfully:", query)

    except Exception as e:
        # 작업 처리 중 오류가 발생하면 예외를 처리하고 로그 등을 남길 수 있습니다.
        print("Error processing job:", e)
    
if __name__=='__main__':
    Insert_Job(query='query')