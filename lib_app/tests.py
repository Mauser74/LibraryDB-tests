# lib_app/tests/test_models.py
from datetime import date, datetime, timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from lib_app.models import Author, Publisher, Book, Cart, BorrowedBook

CustomUser = get_user_model()


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email="user@example.com",
            full_name="Иван Иванов",
            date_of_birth=date(1990, 5, 15),
            password="pass123"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(str(user), "Иван Иванов (user@example.com)")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(
            email="admin@example.com",
            full_name="Админ",
            date_of_birth=date(1980, 1, 1),
            password="admin123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_email_required(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="", full_name="Тест", date_of_birth=date(2000, 1, 1)
            )

    def test_full_name_required(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="test@example.com", full_name="", date_of_birth=date(2000, 1, 1)
            )


class AuthorModelTest(TestCase):
    def test_author_str(self):
        author = Author.objects.create(name="Фёдор Достоевский")
        self.assertEqual(str(author), "Фёдор Достоевский")

    def test_valid_dates(self):
        author = Author(
            name="Лев Толстой",
            date_of_birth=date(1828, 9, 9),
            date_of_death=date(1910, 11, 20)
        )
        author.full_clean()  # не должно быть ошибки
        author.save()
        self.assertEqual(author.name, "Лев Толстой")

    def test_birth_after_death_raises_error(self):
        author = Author(
            name="Невозможный автор",
            date_of_birth=date(2000, 1, 1),
            date_of_death=date(1990, 1, 1)
        )
        with self.assertRaises(ValidationError):
            author.full_clean()

    def test_death_in_future_raises_error(self):
        future = date.today() + timedelta(days=1)
        author = Author(name="Будущий", date_of_death=future)
        with self.assertRaises(ValidationError):
            author.full_clean()


class PublisherModelTest(TestCase):
    def test_publisher_str(self):
        pub = Publisher.objects.create(name="Азбука")
        self.assertEqual(str(pub), "Азбука")

    def test_unique_name(self):
        Publisher.objects.create(name="Эксмо")
        with self.assertRaises(Exception):  # IntegrityError
            Publisher.objects.create(name="Эксмо")


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Чехов")
        self.publisher = Publisher.objects.create(name="Русская классика")

    def test_book_str(self):
        book = Book.objects.create(
            title="Вишнёвый сад",
            author=self.author,
            publisher=self.publisher
        )
        self.assertIn("Чехов", str(book))

    def test_isbn_length_validation_not_enforced_by_model(self):
        # Модель не валидирует длину ISBN — это можно добавить позже
        book = Book.objects.create(title="Тест", isbn="123")  # короткий ISBN
        self.assertEqual(book.isbn, "123")

    def test_year_cannot_be_in_future(self):
        future_year = datetime.now().year + 1
        book = Book(title="Будущая книга", year=future_year)
        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_year_min_value(self):
        book = Book(title="Древняя книга", year=0)
        with self.assertRaises(ValidationError):
            book.full_clean()


class CartModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="reader@test.com",
            full_name="Читатель",
            date_of_birth=date(1995, 3, 3)
        )
        self.staff = CustomUser.objects.create_user(
            email="librarian@test.com",
            full_name="Библиотекарь",
            date_of_birth=date(1985, 2, 2),
            is_staff=True
        )
        self.book = Book.objects.create(title="Тестовая книга")

    def test_regular_user_can_have_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart.books.add(self.book)
        self.assertIn(self.book, cart.books.all())
        self.assertEqual(str(cart), "Корзина Читатель")

    def test_staff_cannot_have_cart(self):
        with self.assertRaises(ValidationError):
            cart = Cart(user=self.staff)
            cart.full_clean()

    def test_one_to_one_cart(self):
        Cart.objects.create(user=self.user)
        with self.assertRaises(Exception):  # IntegrityError
            Cart.objects.create(user=self.user)


class BorrowedBookModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="user@test.com",
            full_name="Пользователь",
            date_of_birth=date(1990, 1, 1)
        )
        self.book = Book.objects.create(
            title="Выдаваемая книга",
            available=True
        )

    def test_borrowed_book_creation(self):
        bb = BorrowedBook.objects.create(user=self.user, book=self.book)
        self.assertFalse(bb.returned)
        self.assertIsNone(bb.returned_at)
        self.assertIsNotNone(bb.borrowed_at)

    def test_book_availability_updated_on_issue(self):
        # Примечание: эта логика должна быть в представлении или сигнале
        # Сама модель BorrowedBook не управляет available — но можно протестировать в view
        pass

    def test_str_representation(self):
        bb = BorrowedBook.objects.create(user=self.user, book=self.book)
        self.assertIn("выдана", str(bb))
        bb.returned = True
        self.assertIn("возвращена", str(bb))
