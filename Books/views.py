from django.shortcuts import render

from rest_framework.response import Response
from .models import Book, Like
from rest_framework import viewsets
from .serializer import BookSerializer
from book_review.utils import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
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
        book = get_object_or_404(Book, id=pk)
        serializer = BookSerializer(book,
             context={'request': request})
        return Response({"data": serializer.data},
                status=status.HTTP_200_OK)
    

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
        
    @action(detail=False, methods=['post'], url_path='like_book')
    def like_book(self, request):
        user = request.user
        book_id = request.data.get("book_id")

        if not book_id:
            return Response({'message': 'Please provide book ID'},
                             status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, id=book_id)

        like, created = Like.objects.get_or_create(user=user, book=book)

        if not created:
            return Response({'message': 'Book already liked'},
                             status=status.HTTP_200_OK)

        return Response({'message': 'Book liked successfully',
                          'total_likes': book.total_likes()},
                            status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='unlike_book')
    def unlike_book(self, request):
        user = request.user
        book_id = request.data.get("book_id")

        if not book_id:
            return Response({'message': 'Please provide book ID'},
                             status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, id=book_id)
        like = Like.objects.filter(user=user, book=book)

        if not like.exists():
            return Response({'message': 'Book not liked'},
                             status=status.HTTP_200_OK)

        like.delete()

        return Response({'message': 'Book unliked successfully',
                          'total_likes': book.total_likes()},
                            status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='get_book_likes')
    def get_book_likes(self, request):
        book_id = request.query_params.get("book_id")

        if not book_id:
            return Response({'message': 'Please provide book ID'},
                             status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, id=book_id)
        likes = Like.objects.filter(book=book)

        if not likes.exists():
            return Response({'message': 'No likes found for this book'},
                             status=status.HTTP_200_OK)

        liked_users = [
            {"id": like.user.id, "username": like.user.username}
            for like in likes
        ]

        return Response({
            "message": "Book likes retrieved successfully",
            "total_likes": book.total_likes(),
            "liked_users": liked_users
        }, status=status.HTTP_200_OK)

