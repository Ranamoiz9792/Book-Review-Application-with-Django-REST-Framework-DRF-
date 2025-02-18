from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'bookdetail        ', BookViewSet, basename='bookdetail')

urlpatterns = [
    path('', include(router.urls)),

    path('bookdetail/like_book/', BookViewSet.as_view({'post': 'like_book'}), name='like-book'),
    path('bookdetail/unlike_book/', BookViewSet.as_view({'post': 'unlike_book'}), name='unlike-book'),
    path('bookdetail/get_book_likes/', BookViewSet.as_view({'get': 'get_book_likes'}), name='get-book-likes'),
]