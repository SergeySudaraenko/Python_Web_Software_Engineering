from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]  # відображення перших 50 символів тексту цитати

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    quotes = models.ManyToManyField(Quote, related_name='tags')

    def __str__(self):
        return self.name


