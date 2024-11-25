from django.db import models
from pgvector.django import VectorField

# Create your models here.

class Category(models.Model):
    code = models.CharField(max_length=3, unique=True, default='CAT')
    name = models.CharField(max_length=30, unique=True)
    embedding = VectorField(dimensions=256)
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500)
    content = models.TextField()
    write_date = models.DateTimeField()
    url = models.URLField(unique=True)
    embedding = VectorField(dimensions=256)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')

    def __str__(self):
        return self.title