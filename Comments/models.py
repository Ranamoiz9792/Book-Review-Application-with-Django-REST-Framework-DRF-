from django.db import models
from Books.models import Book
from Users.models import User
# Create your models here.
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comment')
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content + "on" + self.book.title

