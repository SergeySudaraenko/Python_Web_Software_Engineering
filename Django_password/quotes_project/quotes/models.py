from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    tags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'"{self.text}" - {self.author}'

