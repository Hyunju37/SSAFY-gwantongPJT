from news.models import Category
import dotenv
from openai import OpenAI
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Initialize category embeddings for zero-shot classification'
    def handle(self, *args, **kwargs):
        dotenv_file = dotenv.find_dotenv('/home/hj/final-project/.env')
        CLIENT_ID = dotenv.dotenv_values(dotenv_file)['OPENAI_API_KEY']
        client = OpenAI(api_key=CLIENT_ID)

        CATEGORY_CHOICES = [
            ('LAN', '언어'),
            ('ECO', '경제'),
            ('EDU', '교육'),
            ('POL', '정치'),
            ('CUL', '문화'),
            ('SPT', '스포츠'),
            ('ITS', 'IT및과학'),
            ('SCI', '사회'),
            ('ENT', '연예'),
            ('ENV', '환경'),
            ('TVL', '여행'),
            ('CAR', '자동차')
        ]

        for code, name in CATEGORY_CHOICES:
            embedding = client.embeddings.create(input = [name],
                                    model='text-embedding-3-small',
                                    dimensions=256).data[0].embedding
            
            category, created = Category.objects.update_or_create(
                                    code=code,
                                    defaults={'name': name, 'embedding': embedding})
