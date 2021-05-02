from django.core.exceptions import ValidationError
from backend.otp import TOTPBackend
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)
    otp = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        phone_number, otp = attrs["phone_number"], attrs["otp"]
        totp = TOTPBackend(phone_number=phone_number)
        verify = totp.verify_otp(otp=otp)
        if not verify:
            raise ValidationError("OTP does not match")
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
