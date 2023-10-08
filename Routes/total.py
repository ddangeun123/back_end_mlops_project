from flask import Blueprint, request, jsonify

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

def Search_Market(query:str):
    # 회사정보 테이블에서 마켓정보 가져오기
    return 'NASDAQ'

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
    query = request.args.get('query', '')
    return history_data[query]

if __name__=='__main__':
    predict_bool, predict_price = Search(query='AAPL')
    data = {
        'query':'AAPL',
        'predict_bool':predict_bool,
        'predict_price':predict_price,
    }
    print(Print_test(data=data))