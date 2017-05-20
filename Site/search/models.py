from django.db import models


# Create your models here.
class SearchItem(models.Model):
    title = models.CharField('Title', max_length=120)
    summary = models.TextField('Summary')
    url = models.CharField('URL', max_length=225)

    def __str__(self):
        return self.title
