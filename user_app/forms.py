from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)
from django.contrib.auth import get_user_model

from user_app.models import CustomUser

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации нового пользователя"""

    full_name = forms.CharField(
        max_length=255,
        label="Имя читателя",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите ваше имя"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите e-mail"}
        ),
    )
    date_of_birth = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    class Meta:
        model = User
        fields = ("full_name", "email", "date_of_birth")

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Пользователь с таким e-mail уже зарегистрирован."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.full_name = self.cleaned_data["full_name"]
        user.date_of_birth = self.cleaned_data["date_of_birth"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Форма входа по email и паролю"""

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите e-mail"}
        ),
    )

    def clean_username(self):
        return self.cleaned_data["username"].lower()


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "full_name",
            "email",
            "date_of_birth",
            "is_active",
        )  # ← нет 'password'
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


# class CustomUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = CustomUser
#         fields = ('full_name', 'email', 'date_of_birth', 'is_active')
#         widgets = {
#             'full_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }
