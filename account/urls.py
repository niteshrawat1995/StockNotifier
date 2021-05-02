from django.urls import path

from account.views import LoginView, OTPView, RefreshTokenView

urlpatterns = [
    path("send-otp/", OTPView.as_view()),
    path("login-otp/", LoginView.as_view()),
    path("refresh-token/", RefreshTokenView.as_view()),
]
