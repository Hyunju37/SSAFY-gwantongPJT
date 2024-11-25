from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import status
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import ArticleListSerializer, ArticleSerializer
from .models import Article
import pandas as pd
import dotenv
from openai import OpenAI

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ast
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
    
@api_view(['GET'])
def get_similar_article_by_id(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        article_serializer = ArticleSerializer(article)
        article_embedding = article_serializer.data.get('embedding')
        if isinstance(article_embedding, str):
            # 문자열인 경우: 배열로 변환
            article_embedding = ast.literal_eval(article_embedding)
            print(type(article_embedding))
        elif isinstance(article_embedding, (list, np.ndarray)):
            # 이미 배열인 경우: 그대로 사용
            article_embedding = article.embedding
        if not article_embedding:
            return JsonResponse({'error': 'The article does not have an embedding.'}, status=400)

        all_articles = Article.objects.exclude(pk=pk).all().values()
        df = pd.DataFrame(list(all_articles))
        # all_articles_serializer = ArticleSerializer(all_articles, many=True)
        df['similarities'] = df.embedding.apply(lambda x:cosine_similarity(np.array(article_embedding).reshape(1, -1), np.array(x).reshape(1, -1)))
        res = df.sort_values('similarities', ascending=False).head(5)
        top_articles = Article.objects.filter(id__in=res['id'])
        serializer = ArticleListSerializer(top_articles, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def get_articles_by_category(request):
    try:
        category = request.query_params.get('category', '')
        page = request.query_params.get('page', 1)
        if category == '전체':
            articles = Article.objects.all().order_by('-write_date')
            paginator = Paginator(articles, 6)
            try:
                paginated_articles = paginator.page(page)
            except PageNotAnInteger:
                paginated_articles = paginator.page(1)
            except EmptyPage:
                return Response({'error': 'No more pages'}, status=404)
            serializer = ArticleSerializer(paginated_articles, many=True)
            return Response({
                'page': page,
                'total_pages': paginator.num_pages,
                'total_articles': paginator.count,
                'articles_imageNews': serializer.data[:2],
                'articles_newsCards': serializer.data[2:]
            }, status=200)
        else:
            articles = Article.objects.filter(category__name=category).order_by('-write_date')  # 최신순 정렬
            paginator = Paginator(articles, 6)
            try:
                paginated_articles = paginator.page(page)
            except PageNotAnInteger:
                paginated_articles = paginator.page(1)
            except EmptyPage:
                return Response({'error': 'No more pages'}, status=404)
            serializer = ArticleSerializer(paginated_articles, many=True)
            return Response({
                'page': page,
                'total_pages': paginator.num_pages,
                'total_articles': paginator.count,
                'articles_imageNews': serializer.data[:2],
                'articles_newsCards': serializer.data[2:]
            }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)