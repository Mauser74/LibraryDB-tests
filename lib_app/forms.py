from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import Book, Author, Publisher


class BookModelForm(forms.ModelForm):
    """Форма добавления книги"""

    class Meta:
        model = Book
        # Определяет порядок следования полей на странице
        fields = (
            "title",
            "author",
            "publisher",
            "isbn",
            "year",
            "short_description",
            "key_words",
            "available",
        )
        # Это поле не редактируем
        exclude = ("times_of_issued",)
        # Названия полей
        labels = {
            "title": "Название книги",
            "author": "Автор",
            "publisher": "Издательство",
            "isbn": "ISBN",
            "year": "Год издания",
            "short_description": "Краткое описание",
            "key_words": "Ключевые слова",
            "available": "Доступна для выдачи",
            "times_of_issued": "Выдана раз",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите название"}
            ),
            "author": forms.Select(attrs={"class": "form-control"}),
            "publisher": forms.Select(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 32,
                    "placeholder": "Введите ISBN",
                }
            ),
            "year": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Год издания"}
            ),
            "short_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Краткое описание книги",
                }
            ),
            "key_words": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Введите ключевые слова",
                }
            ),
            "times_of_issued": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Сколько раз книга выдана",
                }
            ),
            "available": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "style": "width: 20px; height: 20px;",
                }
            ),
        }

    def clean_title(self):
        """Валидация названия книги"""
        title = self.cleaned_data.get("title")
        if len(title) > 255:
            raise ValidationError("Слишком длинное название (более 255 символов)")
        elif len(title) == 1:
            raise ValidationError("Название не должно быть пустым")
        return title


class AuthorModelForm(forms.ModelForm):
    """Форма добавления автора"""

    class Meta:
        model = Author
        # Определяет порядок следования полей на странице
        fields = (
            "name",
            "date_of_birth",
            "date_of_death",
        )

        # Названия полей
        labels = {
            "name": "Имя автора",
            "date_of_birth": "Дата рождения",
            "date_of_death": "Дата смерти",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите имя автора"}
            ),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "date_of_death": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
        }

    def clean_date_of_birth(self):
        """Валидация даты рождения"""
        dob = self.cleaned_data.get("date_of_birth")
        if dob and dob > date.today():
            raise ValidationError(
                "Дата рождения не может быть в будущем.", code="birth_in_future"
            )
        return dob

    def clean_date_of_death(self):
        """Валидация даты смерти (только сама по себе)"""
        dod = self.cleaned_data.get("date_of_death")
        if dod and dod > date.today():
            raise ValidationError(
                "Дата смерти не может быть в будущем.", code="death_in_future"
            )
        return dod

    def clean(self):
        """Валидация между полями: дата смерти должна быть > даты рождения"""
        cleaned_data = super().clean()
        dob = cleaned_data.get("date_of_birth")
        dod = cleaned_data.get("date_of_death")

        if dob and dod:
            if dod <= dob:
                raise ValidationError(
                    "Дата смерти не может быть раньше даты рождения.",
                    code="death_before_birth",
                )
        return cleaned_data


class PublisherModelForm(forms.ModelForm):
    """Форма добавления издательства"""

    class Meta:
        model = Publisher
        # Определяет порядок следования полей на странице
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название издательства",
                }
            )
        }
