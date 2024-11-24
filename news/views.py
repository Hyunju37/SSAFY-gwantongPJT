from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import status
from django.http import JsonResponse
from .serializers import ArticleListSerializer, ArticleSerializer
from .models import Article
import pandas as pd
import dotenv
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# Create your views here.

@api_view(['GET'])
def article_list(request):
    query = request.query_params.get('query', '')
    if not query:
        return JsonResponse({'error': 'Query parameter is required'}, status=400)
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
            top_articles = Article.objects.filter(id__in=res['id'])
            serializer = ArticleListSerializer(top_articles, many=True)
            return Response(serializer.data, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_article_by_id(request, pk):
    try:
        # pk에 해당하는 Article 객체를 찾습니다
        article = Article.objects.get(pk=pk)
        # 직렬화하여 반환
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)