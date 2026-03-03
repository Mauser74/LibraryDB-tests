from django.contrib import admin
from .models import Book, Author, Publisher, Cart, BorrowedBook
from user_app.models import CustomUser


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "year",
        "publisher",
        "available",
        "times_of_issued",
    )
    ordering = (
        "author",
        "title",
    )
    search_fields = (
        "title",
        "author__name",
    )
    search_help_text = "Введите часть заголовка или имени автора для поиска в каталоге."
    readonly_fields = ("times_of_issued",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "date_of_birth", "date_of_death")
    ordering = ("name",)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    ordering = ("name",)


@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "borrowed_at", "returned")
    list_filter = ("returned", "borrowed_at")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "books_count")

    @admin.display(description="Книг")
    def books_count(self, obj):
        return obj.books.count()
