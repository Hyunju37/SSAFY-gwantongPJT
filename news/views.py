from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.db.models import Count
from rest_framework import status
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import ArticleListSerializer, ArticleSerializer
from .models import Article
import pandas as pd
import dotenv
from openai import OpenAI
from .services import get_keywords, get_uni_name
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ast
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter
from konlpy.tag import Okt
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
        try:
            uni_names = get_uni_name(article.content)
        except Exception as e:
            uni_names = None
        # 직렬화하여 반환
        serializer = ArticleSerializer(article)
        data = serializer.data
        data['uni_names'] = uni_names
        return Response(data, status=status.HTTP_200_OK)
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
        data = {
            'page': page,
            'total_pages': paginator.num_pages,
            'total_articles': paginator.count,
            'articles_imageNews': serializer.data[:2],
            'articles_newsCards': serializer.data[2:]
        }
        for article in data['articles_newsCards']:
            content = article.get('content', '')
            if content:
                keywords = get_keywords(content)
                article['keywords'] = keywords
            else:
                article['keywords'] = []
        return Response(data, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def news_groupby_category_dashboard(request):
    data = (
        Article.objects.values('category__name')
        .annotate(article_count=Count('id'))
        .order_by('category__name')
    )
    result = list(data)
    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})

@api_view(['GET'])
def wordcloud_dashboard(request):
    try:
        #nltk.download('punkt_tab')
        articles = Article.objects.all()
        all_content = ' '.join([article.content for article in articles])
        print(all_content)
        translator = str.maketrans('', '', string.punctuation)
        all_content = all_content.translate(translator)
        
        okt = Okt()
        #tagged_nouns = okt.pos(all_content, norm=True, stem=True)
        #proper_nouns = [word for word, pos in tagged_nouns if pos == 'Noun']
        #tokens = word_tokenize(all_content)
        korean_stopwords = set([
            '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도',
            '를', '으로', '자', '에', '와', '한', '하다'
        ])
        nouns = okt.nouns(all_content)
        filtered_nouns = [word for word in nouns if word not in korean_stopwords and len(word) > 1]
        word_counts = Counter(filtered_nouns)
        top_n = 100
        most_common = word_counts.most_common(top_n)
        wordcloud_data = [{'name': word, 'value': count} for word, count in most_common]
        return Response(wordcloud_data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['POST'])
def university_chatbot(request):
    message = request.data.get('message', None)
    if message is None:
        # 'message' 키가 없을 경우 에러 응답
        return Response({'error': 'Message not provided'}, status=status.HTTP_400_BAD_REQUEST)
    dotenv_file = dotenv.find_dotenv('/home/hj/final-project/.env')
    CLIENT_ID = dotenv.dotenv_values(dotenv_file)['OPENAI_API_KEY']
    client = OpenAI(api_key=CLIENT_ID)

    msg_embedding = client.embeddings.create(input = [message], 
                                            model='text-embedding-3-small',
                                            dimensions=256).data[0].embedding
    
    articles = Article.objects.all().values()
    df = pd.DataFrame(list(articles))
    df['similarities'] = df.embedding.apply(lambda x:cosine_similarity(np.array(msg_embedding).reshape(1, -1), np.array(x).reshape(1, -1)))
    augid = df.sort_values('similarities', ascending=False).head(1)['id'].values[0]
    aug_article = Article.objects.get(pk=augid).content

    llm = ChatOpenAI(
        model_name='gpt-4o-mini', 
        temperature=0,
        api_key=CLIENT_ID
    )
    system_msg = SystemMessage(
        content=f"당신은 대학교에 관한 최신 이슈와 주요 정보를 제공해 주는 전문가입니다.\
        대학교 입시, 대학원 입시 등을 준비하는 사람들에게 도움을 주어야 합니다.\
        사용자의 질문에 관한 정확한 정보를 전달하는 것이 목적이고, 필요하다면 주어지는 최신 뉴스 기사를 참조할 수 있습니다.\
        만약 사용자가 질문한 특정 대학이 최신 뉴스기사 내용에 포함되지 않거나 관련 없다고 판단된다면 무시해도 됩니다."
    )
    human_msg = HumanMessage(
        content=f'사용자의 질문:{message}\n\n최신 뉴스기사:{aug_article}'
    )
    conversation = [system_msg, human_msg]
    response = llm.invoke(conversation)
    return Response(response.content, status=status.HTTP_200_OK)
