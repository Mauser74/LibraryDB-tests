from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta
from django.conf import settings


class Author(models.Model):
    """Модель автора книги"""

    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        # Порядок сортировки по умолчанию
        ordering = ["name"]

    def clean(self):
        """
        Проверяет логическую корректность дат жизни.
        Вызывается при валидации формы или при вызове full_clean().
        """
        if self.date_of_birth and self.date_of_death:
            if self.date_of_birth > self.date_of_death:
                raise ValidationError("Дата рождения не может быть позже даты смерти.")
        if self.date_of_death and self.date_of_death > date.today():
            raise ValidationError("Дата смерти не может быть в будущем.")

    def save(self, *args, **kwargs):
        """
        Переопределяем save(), чтобы автоматически вызывать валидацию.
        """
        self.full_clean()  # вызывает clean() и другие валидации
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """Модель издательства книги"""

    name = models.CharField("Название издательства", max_length=64, unique=True)

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"
        # Порядок сортировки по умолчанию
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель книги с привязкой к автору"""

    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, related_name="books", null=True, blank=True
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        related_name="books",
        null=True,
        blank=True,
    )
    isbn = models.CharField(
        max_length=13, null=True, blank=True  # ISBN должен содержать ровно 13 цифр
    )
    # Год издания
    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),  # Год должен быть ≥ 1
            MaxValueValidator(datetime.now().year),  # Не больше текущего года
        ],
    )
    # тематические рубрики
    short_description = models.TextField(default="", null=True, blank=True)
    # ключевые слова
    key_words = models.TextField(default="", null=True, blank=True)
    available = models.BooleanField(default=True)  # доступна ли для выдачи
    times_of_issued = models.PositiveIntegerField(default=0)  # сколько раз выдана книга

    def __str__(self):
        return f"{self.author}, {self.title}"


class Cart(models.Model):
    """Корзина пользователя: временный выбор книг перед выдачей"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, blank=True, related_name="carts")

    def clean(self):
        if self.user.is_staff:
            raise ValidationError("Персонал не может иметь корзину.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Корзина {self.user.full_name}"


class BorrowedBook(models.Model):
    """Фактически выданные книги пользователю"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        status = "возвращена" if self.returned else "выдана"
        return f"{self.user.full_name} — {self.book.title} ({status})"
