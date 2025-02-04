from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'published_by', 'cover_image','created_at']
        read_only_fields = ['published_by']
