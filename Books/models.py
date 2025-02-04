from django.db import models
from Users.models import User
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    published_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_books')
    cover_image = models.ImageField(upload_to='static/books-images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " by " + self.author




