from rest_framework import viewsets, status
from rest_framework.response import Response
from book_review.utils import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Book, Reviews
from .serializer import ReviewsSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ReviewsSerializer
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
            return Response({"message": "You cannot Add Review on your own book."},
             status=status.HTTP_401_UNAUTHORIZED)

        serializer = ReviewsSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "message": "Data not valid",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(book=book, user=request.user)

        return Response({
            "message": "Review added successfully",
            "data": serializer.data,
        }, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        review = Reviews.objects.filter(id=pk)
        if not review:
            return Response({"message": "Review not found"},
             status=status.HTTP_404_NOT_FOUND)
        if review.first().user!= request.user:
            return Response({"message": "You cannot update this Review."},
             status=status.HTTP_401_UNAUTHORIZED)
        serializer = ReviewsSerializer(review.first(),
         data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                "message": "Data not valid",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response({
            "message": "Review updated successfully",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        review = Reviews.objects.filter(id=pk)
        if not review:
            return Response({"message": "Review not found"},
             status=status.HTTP_404_NOT_FOUND)
        if review.first().user!= request.user:
            return Response({"message": "You cannot delete this Review."},
             status=status.HTTP_401_UNAUTHORIZED)
        review.delete()

        return Response({
            "message": "Review deleted successfully",
            "data": {},
        }, status=status.HTTP_200_OK)
    def list(self, request):
        try:
            book_id = request.query_params.get('book_id')
            book = Book.objects.filter(pk=book_id).first()

            if not book:
                return Response({'message': 'No book found','data':{}}, status=status.HTTP_200_OK)
            reviews = Reviews.objects.filter(book=book)
            if not reviews:
                return Response({'message': 'No reviews found','data':[]}, status=status.HTTP_200_OK)
            return Response({'message': 'Review Retrive successfully','data': {
                "book_title": book.title,
                "book_author": book.author,
                "reviews": [
                    {   
                        "id": item.id,
                        "user_name": item.user.username,
                        "review": item.review,

                    }
                    for item in reviews
                ]
                }}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
      
        
