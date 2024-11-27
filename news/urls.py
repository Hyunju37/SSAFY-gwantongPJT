from django.urls import path
from . import views

urlpatterns = [
    path('news/search/', views.article_list),
    path('posts/<int:pk>/', views.get_article_by_id),
    path('news/<int:pk>/similar/', views.get_similar_article_by_id),
    path('news/', views.get_articles_by_category),
    path('dashboard/data1/', views.news_groupby_category_dashboard),
    path('dashboard/data2/', views.wordcloud_dashboard),
    path('chatbot/send/', views.university_chatbot),
]
