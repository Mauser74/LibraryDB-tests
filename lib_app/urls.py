from django.urls import path
from . import views
from .views import (
    AuthorListView,
    AuthorCreateView,
    AuthorUpdateView,
    AuthorDeleteView,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    PublisherListView,
    PublisherCreateView,
    PublisherUpdateView,
    PublisherDeleteView,
    CartView,
    AddToCartView,
    RemoveFromCartView,
    IssueBooksFromCartView,
    IndexTemplateView,
    AboutTemplateView,
    UsersWithCartView,
    MyBorrowedBooksView,
    BorrowingUsersListView,
    UserBorrowedBooksListView,
    ReturnBookView,
    StaffViewUserCartView,
    StaffRemoveFromCartView,
)

urlpatterns = [
    path("", IndexTemplateView.as_view(), name="index"),
    path("authors/", AuthorListView.as_view(), name="author_list"),
    path("author/add/", AuthorCreateView.as_view(), name="author_add"),
    path("author/<int:pk>/edit/", AuthorUpdateView.as_view(), name="author_edit"),
    path("author/<int:pk>/delete/", AuthorDeleteView.as_view(), name="author_delete"),
    path("books/", BookListView.as_view(), name="book_list"),
    path("book/add/", BookCreateView.as_view(), name="book_add"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("book/<int:pk>/edit/", BookUpdateView.as_view(), name="book_edit"),
    path("book/<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
    path("publishers/", PublisherListView.as_view(), name="publisher_list"),
    path("publisher/add/", PublisherCreateView.as_view(), name="publisher_add"),
    path(
        "publisher/<int:pk>/edit/", PublisherUpdateView.as_view(), name="publisher_edit"
    ),
    path(
        "publisher/<int:pk>/delete/",
        PublisherDeleteView.as_view(),
        name="publisher_delete",
    ),
    path("cart/", CartView.as_view(), name="view_cart"),
    path("cart/add/<int:book_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path(
        "cart/remove/<int:book_id>/",
        RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
    path(
        "staff/issue-cart/<int:user_id>/",
        IssueBooksFromCartView.as_view(),
        name="issue_books_from_cart",
    ),
    path("staff/users-with-cart/", UsersWithCartView.as_view(), name="users_with_cart"),
    path("my-borrowed/", MyBorrowedBooksView.as_view(), name="my_borrowed_books"),
    path(
        "staff/borrowing-users/",
        BorrowingUsersListView.as_view(),
        name="borrowing_users_list",
    ),
    path(
        "staff/user/<int:user_id>/borrowed/",
        UserBorrowedBooksListView.as_view(),
        name="user_borrowed_books_detail",
    ),
    path(
        "staff/return-book/<int:book_id>/", ReturnBookView.as_view(), name="return_book"
    ),
    path(
        "staff/cart/<int:user_id>/",
        StaffViewUserCartView.as_view(),
        name="staff_view_user_cart",
    ),
    path(
        "staff/cart/<int:user_id>/remove/<int:book_id>/",
        StaffRemoveFromCartView.as_view(),
        name="staff_remove_from_cart",
    ),
    path("about/", AboutTemplateView.as_view(), name="about"),
]
