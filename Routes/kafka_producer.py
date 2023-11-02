from flask import Blueprint, request, jsonify, abort
from Database.db_manager import db_Connection
from Database.redis_manager import Redis_Connection
import json
from datetime import datetime
from confluent_kafka import Producer
# import pytz

app = Blueprint("kafka_producer", __name__)
# time / user_id / Type / Topic
# ​
producer = Producer({'bootstrap.servers': '172.31.7.185:9092,172.31.3.46:9092'})
topic = 'my-topic'
# local_tz = pytz.timezone('Asia/Seoul')

@app.route('/search/predict', methods=['POST'])
def search_predict():
    # 요청에 있는 검색어 가져오기
    search_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = request.args.get('user_id', '')  # 사용자 ID (예: 이메일)
    symbol = request.args.get('query', '')
    search_tab = "predict"

    # 데이터를 JSON 형식으로 준비
    data = {
        'search_time': search_time,
        'user_id': user_id,
        'symbol': symbol,
        'search_tab': search_tab
    }
    
    data = json.dumps(data)
    
    # 데이터를 Kafka Topic으로 전송
    producer.produce(topic, data)
    producer.flush()

@app.route('/search/history', methods=['POST'])
def search_history():
    search_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = request.args.get('user_id', '')  # 사용자 ID (예: 이메일)
    symbol = request.args.get('query', '')
    search_tab = "history"

    data = {
        'search_time': search_time,
        'user_id': user_id,
        'symbol': symbol,
        'search_tab': search_tab
    }
    
    data = json.dumps(data)
    
    producer.produce(topic, data)
    producer.flush()