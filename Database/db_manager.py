import psycopg2
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

# 연결 정보
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),  # 예: 'localhost' 또는 IP 주소
    'port': os.getenv('DB_PORT')  # 예: '5432'
}

def db_Connection():
    print(db_params)
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
    print(db_params)
    conn = db_Connection()
    print(conn)
    conn.close()