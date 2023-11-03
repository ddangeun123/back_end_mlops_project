from flask import Blueprint, request, jsonify, abort
from Database.db_manager import db_Connection
from Database.redis_manager import Redis_Connection

from decimal import Decimal
import json
from datetime import datetime

app = Blueprint("total", __name__)



@app.route('/api/search/predict', methods=['GET'])
def search_predict():
    # 요청에 있는 검색어 가져오기
    symbol = request.args.get('query', '')
    data = Judge_Price(symbol=symbol)

    return data

@app.route('/api/search/history', methods=['GET'])
def search_history():
    q = request.args.get('query', '')
    market = request.args.get('market', 'TOTAL')
    try:
        data = Get_History_Redis(symbol=q)
        return data
    except ValueError as e:
        data = Get_History_Psql(symbol=q, market=market)
        Insert_History_Redis(symbol=q, data=data)
        return jsonify(data)
    
def Get_Predict_DB(symbol:str):
# current_Date = datetime.date()
    query = "SELECT close FROM pred WHERE symbol = %s AND date > %s LIMIT 1"
    try:
        db_conn = db_Connection()
        cursor = db_conn.cursor()
        cursor.execute(query, (symbol, '2023-10-20'))
        result = cursor.fetchall()[0][0]
        cursor.close()
        db_conn.close()
        print(f'predict : {result}')
        return result
    except Exception as e:
        print(f'Get_Predict_DB Error : {e}')
        return None
    
def Get_Price_DB(symbol:str):
    market = Select_Market(symbol=symbol)
    query = f"SELECT close FROM {market} WHERE company_code = %s AND date <= %s LIMIT 1"
    conn = db_Connection()
    cursor = conn.cursor()
    cursor.execute(query, (symbol, '2023-10-20'))
    result = cursor.fetchall()[0][0]
    return result

def Judge_Price(symbol:str):
    predict_price = Get_Predict_DB(symbol=symbol)
    last_price = Get_Price_DB(symbol=symbol)
    if predict_price >= last_price:
        percentage = Calcurate_Percentage(last_price, predict_price)
        message = f'내일 {symbol} 가격은 오를 거에요! 예측 가격은 {predict_price}에요.'
    else:
        percentage = Calcurate_Percentage(last_price, predict_price)
        message = f'내일 {symbol} 가격은 내릴 거에요.. 예측 가격은 {predict_price}에요.'
    data = {
        'symbol':symbol,
        'message':message,
        'percentage':percentage,
    }
    return data

def Calcurate_Percentage(num1, num2):
    if num1 == 0:
        if num2 == 0:
            return 0
        else:
            return float('inf')
    num1 = Decimal(num1)
    num2 = Decimal(num2)
    percentage = ((num2-num1)/num1) * 100
    return percentage


def Query_History(symbol:str, market:str):
    try:
        query = f"""
        SELECT  TO_CHAR(date, 'YYYY-MM-DD') AS formatted_date,
            company_code AS symbol,
            CAST(open AS float) AS open_price,
            CAST(high AS float) AS high_price,
            CAST(low AS float) AS low_price,
            CAST(close AS float) AS close_price,
            CAST(volume AS float) AS volume
        FROM {market.lower()}
        WHERE company_code = %s
        ORDER BY date DESC
        LIMIT 20;"""
        conn = db_Connection()
        cursor = conn.cursor()
        cursor.execute(query, (symbol,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        raise Exception('검색 결과를 찾을 수 없습니다.')

    return result

def Select_Market(symbol:str):
    try:
        query = "SELECT market FROM company WHERE code = %s"
        conn = db_Connection()
        cursor = conn.cursor()
        cursor.execute(query, (symbol,))
        result = cursor.fetchall()[0][0]
        cursor.close()
        conn.close()
    except:
        raise Exception('Cannot Find company by symbol!')
    return result

def Get_History_Redis(symbol:str):
    redis_conn = Redis_Connection()
    data = redis_conn.get(symbol)
    redis_conn.close()
    print(f'redis Data : {data}')
    if data is None:
        raise ValueError('데이터가 없습니다.')
    return data


def Insert_History_Redis(symbol:str, data):
    redis_conn = Redis_Connection()
    try:
        print('Insert Start')
        json_Data = json.dumps(data)
        redis_conn.set(symbol, json_Data)
        result = redis_conn.get(symbol)
        print(f'result : {result}')
    except Exception as e:
        print(e)
    finally:
        redis_conn.close()

def Get_History_Psql(symbol:str, market:str):
    if market=='TOTAL':
        market = Select_Market(symbol=symbol)
    data = Query_History(symbol=symbol, market=market)
    return data

if __name__=='__main__':
    predict_bool, predict_price = Get_Predict_DB(query='AAPL')
    data = {
        'query':'AAPL',
        'predict_bool':predict_bool,
        'predict_price':predict_price,
    }
    print(Print_test(data=data))