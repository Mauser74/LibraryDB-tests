from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, full_name, date_of_birth, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("Пользователь должен иметь e-mail.")
        if not full_name:
            raise ValueError("Пользователь должен иметь имя.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            date_of_birth=date_of_birth,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, full_name, date_of_birth, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(
            email, full_name, date_of_birth, password, **extra_fields
        )


class CustomUser(AbstractUser):
    username = None  # Удаляем username — он не нужен, т.к. аутентификация по email
    # Новое поле: имя читателя
    full_name = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="Имя читателя"
    )

    email = models.EmailField(max_length=255, unique=True, verbose_name="E-mail")

    date_of_birth = models.DateField(
        blank=False, null=False, verbose_name="Дата рождения"
    )

    # Аутентификация по email
    USERNAME_FIELD = "email"
    # Обязательные поля при создании (кроме email и password)
    REQUIRED_FIELDS = ["full_name", "date_of_birth"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} ({self.email})"
