import json
import random
import time
import os
import numpy as np
import pandas as pd
##from sklearn.decomposition import PCA
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from news.models import Article, Category
from django.db import IntegrityError, transaction
import logging
import dotenv
from sklearn.metrics.pairwise import cosine_similarity
# 로깅 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 파일 핸들러 설정
file_handler = logging.FileHandler('crawler.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Command(BaseCommand):
    help = 'Crawl news websites and save articles to the database'

    def handle(self, *args, **kwargs):
        # 데이터 소스 경로
        base_directory = 'raw_data'

        # 크롤링 함수 정의
        def load_one_json_file_and_merge(json_path):
            all_data = []
            if os.path.isfile(json_path) and json_path.endswith('.json'):
                with open(json_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if 'SJML' in data and 'text' in data['SJML']:
                        for text_item in data['SJML']['text']:
                            all_data.append(text_item)
            else:
                logger.warning(f"유효하지 않은 파일 경로 또는 JSON 파일이 아님: {json_path}")
            return all_data

        def collect_data_and_store_json_file(base_directory, query):
            # 네이버 API 인증 정보
            dotenv_file = dotenv.find_dotenv('/home/hj/final-project/.env')

            CLIENT_ID = dotenv.dotenv_values(dotenv_file)['NVR_CLIENT_ID']  # 네이버 개발자 센터에서 발급받은 Client ID
            CLIENT_SECRET = dotenv.dotenv_values(dotenv_file)['NVR_CLIENT_SECRET']       # 네이버 개발자 센터에서 발급받은 Client Secret

            # 검색어 설정 (예: '대학교')
            encoded_query = requests.utils.quote(query)

            # API 요청 URL 기본 설정
            base_url = 'https://openapi.naver.com/v1/search/news.json'

            # 헤더 설정
            headers = {
                'X-Naver-Client-Id': CLIENT_ID,
                'X-Naver-Client-Secret': CLIENT_SECRET
            }

            # 최대 기사 수와 한 번에 가져올 기사 수 설정
            # MAX_ARTICLES = 30
            DISPLAY = 10  # 한 번에 가져올 기사 수 (최대 100개)
            valid_news_count = 0
            start = 1
            # 뉴스 데이터 저장 리스트
            news_list = []
            while valid_news_count < 100:
                url = f'{base_url}?query={encoded_query}&display={DISPLAY}&start={start}'
            # for start in range(1, MAX_ARTICLES + 1, DISPLAY):
            #     # API 요청 URL 구성
            #     url = f'{base_url}?query={encoded_query}&display={DISPLAY}&start={start}'

                # 뉴스 데이터 요청
                response = requests.get(url, headers=headers)

                if response.status_code != 200:
                    logger.error(f"Error Code: {response.status_code}")
                    break

                data = response.json()

                for item in data.get('items', []):
                    link = BeautifulSoup(item.get('link'), 'html.parser').get_text()
                    if link.startswith('https://n.news.naver.com'):
                        title = BeautifulSoup(item.get('title'), 'html.parser').get_text()
                        subtitle = BeautifulSoup(item.get('description', ''), 'html.parser').get_text()
                        #link = BeautifulSoup(item.get('originallink'), 'html.parser').get_text()
                        pub_date = BeautifulSoup(item.get('pubDate'), 'html.parser').get_text()

                        # 뉴스 내용 가져오기
                        try:
                            news_response = requests.get(link, timeout=10)
                            if news_response.status_code == 200:
                                soup = BeautifulSoup(news_response.text, 'html.parser')
                                # 뉴스 사이트마다 내용이 다르므로 적절한 태그 선택 필요
                                # content = ''
                                # article_div = soup.find('div', {'id': 'articleBodyContents'})
                                article = soup.find('article', {'id': 'dic_area'})
                                if article:
                                    content = article.get_text(separator='\n').strip()
                                    content = content.replace('\n','')
                                else:
                                    paragraphs = soup.find_all('p')
                                    content = '\n'.join([p.get_text() for p in paragraphs])
                                # if article_div:
                                #     content = article_div.get_text(separator='\n').strip()
                                # else:
                                #     paragraphs = soup.find_all('p')
                                #     content = '\n'.join([p.get_text() for p in paragraphs])
                            else:
                                logger.warning(f"Unable to retrieve content from {link}: Status Code {news_response.status_code}")
                        except Exception as e:
                            logger.error(f"Failed to retrieve content from {link}: {e}")
                            #content = ''

                        # pub_date 형식 변환
                        try:
                            parsed_date = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
                            formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                        except Exception as e:
                            logger.error(f"Failed to parse pubDate '{pub_date}': {e}")
                            formatted_date = pub_date  # 변환 실패 시 원본 값 사용

                        news_list.append({
                            'title': title,
                            'subtitle': subtitle,
                            'content': content,
                            'write_date': formatted_date,
                            'url': link
                        })
                        valid_news_count += 1
                        if valid_news_count >= 100:
                            break
                    # API 호출 제한을 피하기 위해 잠시 대기
                    time.sleep(0.5)
                start += DISPLAY
                # API 호출 후 현재 저장된 기사 수 출력
                logger.info(f"Retrieved {len(news_list)} articles so far...")

                # 최대 기사를 다 가져오면 중지
                # if len(news_list) >= MAX_ARTICLES:
                #     break

            # JSON 구조 생성
            json_data = {
                "SJML": {
                    "text": news_list  # 최대 MAX_ARTICLES만 저장
                }
            }

            # JSON 파일로 저장
            os.makedirs(base_directory, exist_ok=True)
            json_file_path = os.path.join(base_directory, 'university_news.json')
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

            logger.info("JSON 파일이 성공적으로 생성되었습니다.")
            return json_file_path

        def get_embedding(text):
            dotenv_file = dotenv.find_dotenv('/home/hj/final-project/.env')
            CLIENT_ID = dotenv.dotenv_values(dotenv_file)['OPENAI_API_KEY']

            client = OpenAI(api_key=CLIENT_ID)
            text = text.replace("\n", " ")
            return client.embeddings.create(input = [text], 
                                            model='text-embedding-3-small',
                                            dimensions=256).data[0].embedding

        # 크롤링 실행
        json_file_path = collect_data_and_store_json_file(base_directory, '대학교')

        # 데이터 로드 및 병합
        merged_data_list = load_one_json_file_and_merge(json_file_path)

        # 랜덤으로 데이터 추출 (필요에 따라 조정 가능)
        # data_list = random.sample(merged_data_list, min(30, len(merged_data_list)))

        # 처리된 데이터 개수 출력
        logger.info(f"총 {len(merged_data_list)}개의 뉴스 데이터를 처리합니다.")

        # 모든 데이터를 순회하며 저장

        category_embeddings = Category.objects.all().values()
        cat_df = pd.DataFrame(list(category_embeddings))

        articles_to_create = []
        for data in merged_data_list:
            # pub_date 변환
            write_date = data.get('write_date')
            if isinstance(write_date, str):
                try:
                    write_date = datetime.strptime(write_date, '%Y-%m-%d %H:%M:%S')
                except:
                    write_date = datetime.now()

            embedding = get_embedding(text=f"{data.get('title', 'No Title')} {data.get('subtitle', '')}")
            cat_df['similarities'] = cat_df.embedding.apply(lambda x:cosine_similarity(np.array(embedding).reshape(1, -1), np.array(x).reshape(1, -1)))
            top_cat = cat_df.sort_values('similarities', ascending=False).head(1)['code'].values[0]
            article_category = Category.objects.get(code=top_cat)
            article = Article(
                title=data.get('title', 'No Title'),
                subtitle=data.get('subtitle', ''),
                content=data.get('content', ''),
                write_date=write_date,
                url=data.get('url', ''),
                embedding = embedding,
                category = article_category,
            )
            articles_to_create.append(article)

        # 데이터베이스에 저장 (bulk_create 사용)
        try:
            with transaction.atomic():
                Article.objects.bulk_create(articles_to_create, ignore_conflicts=True)
            logger.info(f"Successfully inserted {len(articles_to_create)} articles into the database.")
        except Exception as e:
            logger.error(f"Failed to insert articles into the database: {e}")

        self.stdout.write(self.style.SUCCESS("Crawling and data storage completed successfully."))