from rest_framework import viewsets, status
from rest_framework.response import Response
from book_review.utils import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Book, Comment
from .serializer import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for handling book comments."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer

    def create(self, request):
        data = request.data
        book_id = data.get('book_id')

        if not book_id:
            return Response({"message": "Book ID is required"},
             status=status.HTTP_400_BAD_REQUEST)

        book = Book.objects.filter(id=book_id).first()
        if not book:
            return Response({"message": "Book not found"},
             status=status.HTTP_404_NOT_FOUND)

        if book.published_by == request.user:
            return Response({"message": "You cannot comment on your own book."},
             status=status.HTTP_401_UNAUTHORIZED)

        serializer = CommentSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "message": "Data not valid",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(book=book, user=request.user)

        return Response({
            "message": "Comment added successfully",
            "data": serializer.data,
        }, status=status.HTTP_201_CREATED)
