from django.shortcuts import render

from rest_framework.response import Response
from .models import Book
from rest_framework import viewsets
from .serializer import BookSerializer
from book_review.utils import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
class BookPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 50
class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = BookPagination
    
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

    # def list(self, request):
    #     try:
    #         books = Book.objects.all()
    #         if books:
    #             return Response({
    #                 "message" : "Books Found",
    #                 "Books" : [
    #                     {
    #                      'id': book.id,
    #                      'title': book.title,
    #                      'description':book.description,
    #                     'author': book.author,
    #                     'published_by': book.published_by.username,
    #                     'cover_image': book.cover_image.url,
    #                     'created_at' : book.created_at,

    #                 }
    #                 for book in books
    #             ]
    #             })
            
    #     except Book.DoesNotExist:
    #         return Response({
    #             "message" : "No books found",
    #         })
    

    def list(self, request):
        try:
            books = Book.objects.all()
            paginator = self.pagination_class()
            paginated_books = paginator.paginate_queryset(books, request)
            if paginated_books:
                return paginator.get_paginated_response({
                    "message" : "Books Found",
                    "Books" : [
                        {
                         'id': book.id,
                         'title': book.title,
                         'description':book.description,
                        'author': book.author,
                        'published_by': book.published_by.username,
                        'cover_image': book.cover_image.url,
                        'created_at' : book.created_at,

                    }
                   for book in paginated_books
                ]
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

    

