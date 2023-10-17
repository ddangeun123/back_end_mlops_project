from flask import Blueprint, request, jsonify, session
from Database.db_manager import db_Connection
import secrets

app = Blueprint("auth", __name__)

@app.route('/auth/userCheck', methods=['POST'])
def Login_User(email:str, password:str):
    email = request.form.get('email')
    password = request.form.get('password')

@app.route('/auth/signup', methods=['POST'])
def Post_User(email:str, password:str):
    email = request.form.get('email')
    password = request.form.get('password')
    session_id = secrets.token_hex(6)
    print(email, password, session_id)
    try:
        UserInsert(email=email, password=password, session_id=session_id)
        data = {
            'success':True,
        }
    except:
        data = {
            'success':False,
        }
    return data
    

def UserCheck():
    conn = db_Connection()

def UserInsert(email:str, password:str, session_id:str):
    conn = db_Connection()
    cursor = conn.cursor()
    query = """
            INSERT INTO usr (email, password, session_id)
            VALUES (%s, %s, %s)
            """
    cursor.execute(query, (email, password, session_id))
    conn.commit()
    cursor.close()
    conn.close()

