from django.urls import path
from .views import (
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
    UserListView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("staff/users/", UserListView.as_view(), name="user_list"),
    path("staff/user/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
    path("staff/user/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
]
