from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, ConfirmRegistrationView, UserPasswordResetView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('confirm-registration/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm_registration'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

]