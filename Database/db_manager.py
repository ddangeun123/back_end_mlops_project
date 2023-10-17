import psycopg2
import os

class Config:
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')

# 연결 정보
db_params = {
    'dbname': 'test01',
    'user': 'manager',
    'password': 'tPZm7M7gAC8UKeNAf3yf',
    'host': '43.201.204.226',  # 예: 'localhost' 또는 IP 주소
    'port': '5432'  # 예: '5432'
}

redis_params = {
    'host':'43.201.204.226',
    'port':6379,
    'db':0
}
def db_Connection():
    return psycopg2.connect(**db_params)

def execute_query(query:str):
    conn = db_Connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    print(f'{query} Execute Done.')

if __name__=='__main__':
    # PostgreSQL 데이터베이스에 연결
    conn = db_Connection()
    print(conn)
    conn.close()
