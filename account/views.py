from rest_framework_simplejwt.views import TokenRefreshView
from account.serializers import LoginSerializer, OTPSerializer, UserSerializer
from backend import otp, twilio
from rest_framework import generics, serializers, views, response
from django.contrib.auth import get_user_model


User = get_user_model()


class OTPView(views.APIView):
    serializer_class = OTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        otp_be = otp.TOTPBackend(phone_number)
        send_status, otp_number = otp_be.send_otp(communication=twilio.Twilio())
        return response.Response(
            data={"send_status": send_status, "otp": otp_number}, status=200
        )


class LoginView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return response.Response(
                {"error": f"No user present with number {phone_number}"}
            )
        user_data = UserSerializer(user).data
        tokens = user.get_token()
        response_data = {"tokens": tokens, "user_data": user_data}
        return response.Response(data=response_data, status=200)


class RefreshTokenView(TokenRefreshView):
    pass
