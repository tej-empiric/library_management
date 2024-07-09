from rest_framework.response import Response
from rest_framework import generics
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework import views
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse


# class IsAdminOrOwner(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.user and request.user.is_staff:
#             return True

#         if request.method in permissions.SAFE_METHODS:
#             return obj.user == request.user

#         if request.method == "PATCH":
#             return obj.user == request.user and request.data.get("return_date")

#         return False


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            refreshToken = RefreshToken(refresh_token)
            refreshToken.blacklist()

            return Response(
                {"Log out successfull."}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {f"Error in Log out. {str(e)}, {status.HTTP_400_BAD_REQUEST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class StaffView(generics.ListAPIView):
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser == True:
            return CustomUser.objects.filter(role="staff")
        else:
            raise PermissionDenied("You do not have permission to perform this action.")


class StaffUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role="staff")
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(email=self.request.user)


class BookAddView(generics.CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("author", "genre")
    search_fields = ["title", "author", "isbn"]


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BorrowBookView(generics.CreateAPIView):
    serializer_class = BorrowedBooksSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book does not exist"})

        if book.is_available == False:
            return Response({"Book is not available to borrow."})

        borrowed_book = BorrowedBooks.objects.create(user=self.request.user, book=book)

        serializer = self.get_serializer(borrowed_book)

        book.is_available = False
        book.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReturnBookView(generics.UpdateAPIView):
    queryset = BorrowedBooks.objects.all()
    serializer_class = BorrowedBooksSerializer
    permission_classes = [permissions.IsAdminUser]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_return_date = request.data.get("return_date")

        if new_return_date is not None and new_return_date >= instance.borrow_date:
            instance.return_date = new_return_date
            instance.save()
        else:
            return Response({"error": "Please enter a return date."})

        serializer = self.get_serializer(instance)

        book = instance.book
        book.is_available = True
        book.save()

        # TODO: notify user who has reserved the book. django chl

        return Response(serializer.data)


class ListBorrowedBooksView(generics.ListAPIView):
    queryset = BorrowedBooks.objects.all()
    serializer_class = BorrowedBooksSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return BorrowedBooks.objects.all().order_by("-borrow_date")
        else:
            return BorrowedBooks.objects.filter(user=self.request.user).order_by(
                "-borrow_date"
            )


# reservation class

# # notification class(generics.ListAPIView):
#    def get_queryset(self):
#         return Notification.objects.filter(user=self.request.user).order_by("-created_at")
