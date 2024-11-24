from django.urls import path
from . import views

urlpatterns = [
    path('news/search/', views.article_list),
    path('posts/<int:pk>/', views.get_article_by_id),
]
