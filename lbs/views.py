from django.contrib.auth import get_user_model
from rest_framework import status, generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Book, Enrollment
from .serializers import UserRegistrationSerializer, UserLoginSerializer, BookSerializer, EnrollmentSerializer
from .permissions import IsAdminOrReadOnly, IsLibrarian
from .utils import send_enrollment_email

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({
            "message": "Login successful",
            "access": serializer.validated_data['access'],
            "refresh": serializer.validated_data['refresh'],
            "email": user.email,
            "role": user.role
        }, status=status.HTTP_200_OK)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Book '{instance.title}' deleted successfully."},
            status=status.HTTP_200_OK
        )


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsLibrarian]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [perm() for perm in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'LIBRARIAN']:
            return Enrollment.objects.all()
        else:
            return Enrollment.objects.filter(user=user)

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if not book.is_available:
            raise ValidationError(f"Book '{book.title}' is currently unavailable.")

        enrollment = serializer.save()

        book.is_available = False
        book.save()

        admin_emails = list(User.objects.filter(role='ADMIN').values_list('email', flat=True))

        try:
            send_enrollment_email(
                subject=f"Book Enrollment Confirmation: {book.title}",
                core_message=f"The book '{book.title}' has been enrolled successfully\n",
                book_title=book.title,
                user_email=enrollment.user.email,
                start_date=enrollment.start_date,
                end_date=enrollment.end_date,
                admin_emails=admin_emails
            )
        except Exception as e:
            print(f"Email failed: {e}")

        return enrollment
