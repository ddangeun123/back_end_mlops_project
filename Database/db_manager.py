import psycopg2
import os

class Config:
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')

config = Config()
# 연결 정보
db_params = {
    'dbname': config.DB_NAME,
    'user': config.DB_USER,
    'password': config.DB_PASSWORD,
    'host': config.DB_HOST,  # 예: 'localhost' 또는 IP 주소
    'port': config.DB_PORT  # 예: '5432'
}
# testDB
# db_params = {
#     'dbname': 'test01',
#     'user': 'manager',
#     'password': 'qwer1234',
#     'host': '127.0.0.1',  # 예: 'localhost' 또는 IP 주소
#     'port': '5432'  # 예: '5432'
# }

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
    print(db_params)
    conn = db_Connection()
    print(conn)
    conn.close()
