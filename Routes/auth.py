from flask import Blueprint, request, jsonify, sessin
from werkzeug import security
from Database.db_manager import db_Connection
import secrets

app = Blueprint("auth", __name__)

@app.route('/api/auth/signup', methods=['POST'])
def SignUp_User():
    data = request.json

    # 데이터 검증 및 처리 로직을 추가
    email = data.get('email')
    password = data.get('password')

    user_exist = UserCheck(email=email)
    if user_exist:
        return CreateResponse(False, email, '이미 존재하는 이메일입니다.')
    hashed_password = security.generate_password_hash(password)
    session_id = secrets.token_hex(6)
    try:
        DB_result = UserInsert(email=email, password=hashed_password, session_id=session_id)
        return CreateResponse(True, email, '회원가입 성공')
    except Exception as e:
        print(e)
    return CreateResponse(False, email, '알 수 없는 오류. 잠시 후 >시도해주세요.')

@app.route('/api/auth/login', methods=['POST'])
def Login_User():
    data = request.json

    email = data.get('email')
    password = data.get('password')
    sessionID = secrets.token_hex(6)

    successed, message = ExistUserCheck(email=email, password=password)
    return CreateResponse(success=successed, email=email, message=message)

def CreateResponse(success:bool, email:str, message:str):
    data = {
        'success':success,
        'email':email,
        'message':message,
    }
    return jsonify(data)

def GetUser(email:str):
    query = "SELECT email, password FROM user_info WHERE email = %s;"
    conn = db_Connection()
    cursor = conn.cursor()
    cursor.execute(query, (email, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def UserCheck(email:str):
    result = GetUser(email=email)
    if len(result)>0:
        return True
    else:
        return False

def ExistUserCheck(email:str, password:str):
    result = GetUser(email=email)
    print(result)
    if len(result)>0:
        if security.check_password_hash(result[0][1], password):
            return True, '로그인 성공'
        else:
            return False, '비밀번호가 일치하지 않습니다.'
    else:
        return False, '가입된 이메일이 존재하지 않습니다.'

def UserInsert(email:str, password:str, session_id:str):
    query = """
            INSERT INTO user_info (email, password, session_id)
            VALUES (%s, %s, %s)
            """
    conn = db_Connection()
    cursor = conn.cursor()
    result = cursor.execute(query, (email, password, session_id))
    print(f'result : {result}')
    conn.commit()
    cursor.close()
    conn.close()
    return result