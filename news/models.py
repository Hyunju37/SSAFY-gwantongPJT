from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500)
    content = models.TextField()
    write_date = models.DateTimeField()
    url = models.URLField(unique=True)

    def __str__(self):
        return self.title