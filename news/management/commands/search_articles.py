import logging
from django.core.management.base import BaseCommand, CommandParser
from news.models import Article
import pandas as pd
import dotenv
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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
    
    def add_arguments(self, parser):
        parser.add_argument('major', type=str, help='input major name')

    
    def handle(self, *args, **kwargs):
        query = kwargs['major']

        try:
            dotenv_file = dotenv.find_dotenv('/home/hj/final-project/.env')
            CLIENT_ID = dotenv.dotenv_values(dotenv_file)['OPENAI_API_KEY']
            client = OpenAI(api_key=CLIENT_ID)

            query_embedding = client.embeddings.create(input = [query], 
                                                    model='text-embedding-3-small',
                                                    dimensions=256).data[0].embedding
            articles = Article.objects.all().values()
            df = pd.DataFrame(list(articles))
            df['similarities'] = df.embedding.apply(lambda x:cosine_similarity(np.array(query_embedding).reshape(1, -1), np.array(x).reshape(1, -1)))
            res = df.sort_values('similarities', ascending=False).head(3)
            print(res)
            self.stdout.write(self.style.SUCCESS("Successfully loaded data into DataFrame"))
            
        except Exception as e:
            logger.error(f"Error loading articles: {e}")
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
