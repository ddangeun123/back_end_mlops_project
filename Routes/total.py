from flask import Blueprint, request, jsonify
from Database.db_manager import db_Connection

app = Blueprint("total", __name__)

stock_data={
    'AAPL':{'predict':177.49},
}
history_data={
    'AAPL':{
        'date':'2023-10-08',
        'symbol':'AAPL',
        'open':176.80,
        'high':180.02,
        'low':172.65,
        'close':179.42,
        'volume':142.026,
    },
}
company_info={
    'symbol':'AAPL',
    'company_name':'애플',
    'market':'NASDAQ',
}
markets=['AMEX', 'NYSE', 'NASDAQ', 'TOTAL']

def Search(query:str, market:str = 'TOTAL'):
    # 예상 가격 테이블에서 쿼리
    estimated_price = stock_data[query]['predict']
    # 어제 종가 쿼리
    yester_day_price = history_data[query]['close']
    return (yester_day_price < estimated_price), estimated_price

def Print_test(data):
    if data['predict_bool']:
        message = '오를거에요'
    else:
        message = '내릴거에요'
    query = data['query']
    predict_price = data['predict_price']
    result = f'{query}은 내일 {message}. 예상가격은 {predict_price}에요!'
    return result

@app.route('/search/predict', methods=['GET'])
def search_total():
    # 요청에 있는 검색어 가져오기
    query = request.args.get('query', '')
    market = request.args.get('market', '')
    if market == 'TOTAL':
        market = Search_Market(query=query)
    # DB에서 검색결과 가져오기
    predict_bool, predict_price = Search(query=query, market=market)
    result = {
        'query':query,
        'predict_bool':predict_bool,
        'predict_price':predict_price
    }
    return result

@app.route('/search/history', methods=['GET'])
def search_history():
    q = request.args.get('query', '')
    market = request.args.get('market', 'TOTAL')
    if market=='TOTAL':
        market = Select_Market(symbol=q)
    data = DB_GetHistory(q=q, market=market)
    json_data = jsonify(data)
    print(json_data)
    return json_data

def DB_GetHistory(q:str, market:str):
    try:
        if market == 'nyse':
            query = """SELECT
            TO_CHAR(date, 'YYYY-MM-DD') AS formatted_date,
            company_code AS symbol,
            ROUND(open, 2) AS open_price,
            ROUND(high, 2) AS high_price,
            ROUND(low, 2) AS low_price,
            ROUND(close, 2) AS close_price,
            volume
            FROM nyse WHERE company_code = %s 
            ORDER BY date DESC
            limit 20;"""
        elif market == 'nasdaq':
            query = """SELECT
            TO_CHAR(date, 'YYYY-MM-DD') AS formatted_date,
            company_code AS symbol,
            ROUND(open, 2) AS open_price,
            ROUND(high, 2) AS high_price,
            ROUND(low, 2) AS low_price,
            ROUND(close, 2) AS close_price,
            volume AS volume
            FROM nasdaq WHERE company_code = %s
            ORDER BY date DESC
            limit 20;"""
        elif market == 'amex':
            query = """SELECT
            TO_CHAR(date, 'YYYY-MM-DD') AS formatted_date,
            company_code AS symbol,
            ROUND(open, 2) AS open_price,
            ROUND(high, 2) AS high_price,
            ROUND(low, 2) AS low_price,
            ROUND(close, 2) AS close_price,
            volume AS volume
            FROM amex WHERE company_code = %s
            ORDER BY date DESC
            limit 20;"""
        conn = db_Connection()
        cursor = conn.cursor()
        cursor.execute(query, (q,))
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

if __name__=='__main__':
    predict_bool, predict_price = Search(query='AAPL')
    data = {
        'query':'AAPL',
        'predict_bool':predict_bool,
        'predict_price':predict_price,
    }
    print(Print_test(data=data))