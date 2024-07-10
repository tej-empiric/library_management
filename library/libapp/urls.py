from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin/staff/", StaffView.as_view(), name="staff"),
    path("admin/staff/<int:pk>/", StaffUpdateView.as_view(), name="staff_update"),
    path("user/", UserDetailView.as_view(), name="user"),
    path("user/<int:pk>/", UserUpdateView.as_view(), name="user"),
    path("book/add/", BookAddView.as_view(), name="book_add"),
    path("book/update/<int:pk>/", BookUpdateView.as_view(), name="book_update"),
    path("book/delete/<int:pk>/", BookDeleteView.as_view(), name="book_delete"),
    path("book/list/", BookListView.as_view(), name="book_list"),
    path("book/detail/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("borrow/", BorrowBookView.as_view(), name="borrow_book"),
    path("return/<int:pk>/", ReturnBookView.as_view(), name="return_book"),
    path("list/borrowed/", ListBorrowedBooksView.as_view(), name="list_borrowed_books"),
    path("reserve/", ReserveBookView.as_view(), name="reserve_book"),
    path("list/reserve/", ListReserveBookView.as_view(), name="list_reserve_books"),
]
