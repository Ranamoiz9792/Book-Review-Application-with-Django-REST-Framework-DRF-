from django.db import models

from Users.models import User
from Books.models import Book

class Reviews(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_reviews')
    review = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_reviews')
    created_at= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.review + "on" + self.book.title
    