import os
from confluent_kafka import Consumer, KafkaError
from hdfs import InsecureClient
import pandas as pd

# Kafka Consumer 설정
consumer_conf = {
    'bootstrap.servers': '172.31.7.185:9092,172.31.3.46:9092',
    'group.id': 'user_info',
    'auto.offset.reset': 'earliest'
}

def send_data_to_hadoop(df):
    # 데이터를 Hadoop으로 전송하는 로직을 여기에 추가
    # 예를 들어, HDFS에 저장하거나 Hadoop MapReduce 작업을 실행하는 방식으로 전송 가능

    # HDFS에 데이터 저장하는 예제
    hdfs_client = InsecureClient(os.environ.get('HADOOP_HOST'))
    hdfs_upload_path = f'/home/ubuntu/test/{count}_user_session.csv'

    # HDFS에 저장
    with hdfs_client.write(hdfs_upload_path, overwrite=True) as writer:
        df.to_csv(writer, index=False)

# Kafka Topic 및 큐 설정
topic = 'my-topic'
data_queue = []
batch_size = 100  # 데이터를 모을 크기

# Kafka Consumer를 초기화
consumer = Consumer(consumer_conf)
consumer.subscribe([topic])
count = 0

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('Reached end of partition')
        else:
            print('Error: {}'.format(msg.error()))
    else:
        data = msg.value().decode('utf-8')  # Kafka로부터 데이터 가져오기
        data_queue.append(data)  # 데이터를 큐에 추가
        print("큐 추가")
        if len(data_queue) >= batch_size:
            # 데이터 프레임 생성
            df = pd.DataFrame(data_queue)
            count += 1
            send_data_to_hadoop(df)  # 데이터가 일정량 모였을 때 Hadoop으로 전송
            data_queue.clear()
            print("적재")