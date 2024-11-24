from rest_framework import serializers
from .models import Article

class ArticleListSerializer(serializers.ModelSerializer):
    write_date = serializers.DateTimeField(format='%Y-%m-%d')  # 날짜 형식으로 포맷팅
    class Meta:
        model = Article
        fields = ('id', 'title', 'subtitle', 'write_date')

class ArticleSerializer(serializers.ModelSerializer):
    write_date = serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = Article
        fields = '__all__'