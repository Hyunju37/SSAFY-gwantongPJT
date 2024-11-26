import json
import os
from hdfs import InsecureClient
from datetime import datetime
import time

hdfs_client = InsecureClient('http://localhost:9870', user='hj')  # 'localhost'와 'hadoop-user' 부분을 환경에 맞게 수정하세요.
hdfs_path = '/user/news/realtime/'  # HDFS 내 데이터 저장 경로
json_file_path = 'raw_data/university_news.json'

def load_one_json_file_and_merge(json_path):
    all_data = []
    if os.path.isfile(json_path) and json_path.endswith('.json'):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'SJML' in data and 'text' in data['SJML']:
                for text_item in data['SJML']['text']:
                    all_data.append(text_item)
    else:
        print(f"유효하지 않은 파일 경로 또는 JSON 파일이 아님: {json_path}")
    return all_data

merged_data_list = load_one_json_file_and_merge(json_file_path)

for data in merged_data_list:
    json_data = json.dumps(data, ensure_ascii=False)
    file_name = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    print(json_data)
    print(hdfs_path + file_name)
    # breakpoint()
    # HDFS에 데이터 저장
    with hdfs_client.write(hdfs_path + file_name, encoding='utf-8') as writer:
        writer.write(json_data)
    
    # 저장된 파일 경로 출력
    print(f"Data sent to HDFS: {hdfs_path + file_name}")
    
    # 1초 대기 (데이터 전송 간격)
    time.sleep(1)