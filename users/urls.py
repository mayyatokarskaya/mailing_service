from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import VerifiedLoginView, UserListView, toggle_block_user, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path("register/", views.register, name="register"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),
        name="password_reset",
    ),
    path("verify/<int:user_id>/", views.verify_email, name="verify_email"),
    path("login/", VerifiedLoginView.as_view(template_name="registration/login.html"), name="login"),
]

urlpatterns += [
    path("user-list/", UserListView.as_view(), name="user_list"),
    path("block-user/<int:user_id>/", toggle_block_user, name="block_user"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]


urlpatterns += [

]