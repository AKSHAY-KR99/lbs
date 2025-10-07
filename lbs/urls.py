from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from lbs.views import UserRegistrationView, UserLoginView, BookViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login')
] + router.urls
