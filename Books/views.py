from django.shortcuts import render

from rest_framework.response import Response
from .models import Book
from rest_framework import viewsets
from .serializer import BookSerializer
from book_review.utils import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def create(self, request):
        data=request.data
        user = request.user
        serializer = BookSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "message" : "Data not valid",
                "errors" : serializer.errors,   
            })
        serializer.save(
            published_by=user
        )
        return Response({
            "message" : "Data Saved Successfully",
            "data" : serializer.data,
        })

    def list(self, request):
        try:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response({
            "data" :  serializer.data,

                })
        except Book.DoesNotExist:
            return Response({
                "message" : "No books found",
            })
        
    def retrieve(self, request, pk=None):
        try:
            book = Book.objects.get(id=pk)
            serializer = BookSerializer(book)
            return Response({
                "data" : serializer.data,
            })
        except Book.DoesNotExist:
            return Response({
                "message" : "Book not found",
            })
    def partial_update(self, request, pk=None):
        try:
            book = Book.objects.get(id=pk)
            data = request.data
            serializer = BookSerializer(book, data=data, partial=True)
            if not serializer.is_valid():
                return Response({
                    "message" : "Data not valid",
                    "errors" : serializer.errors,   
                })
            serializer.save()
            return Response({
                "message" : "Data Saved Successfully",
                "data" : serializer.data,
            })
        except Book.DoesNotExist:
            return Response({
                "message" : "Book not found",
            })
    def destroy(self, request, pk=None):
        try:
            book = Book.objects.get(id=pk)
            book.delete()
            return Response({
                "message": "Book deleted successfully",
                "data": {}
            }, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({
                "message": "Book not found",
            }, status=status.HTTP_404_NOT_FOUND)

    

