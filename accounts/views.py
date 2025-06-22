from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import (
    UserRegisterSerializer,
    OTPRequestSerializer,
    OTPVerificationSerializer,
)
from rest_framework.response import Response
from rest_framework import status
import pyotp
from django.core.mail import send_mail
from django.conf import settings
from .models import User, OTP

# Create your views here.


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            #  Generate OTP secret + code
            otp_secret = pyotp.random_base32()
            totp = pyotp.TOTP(otp_secret, interval=600)
            otp_code = totp.now()

            #  Save OTP record
            OTP.objects.filter(user=user, is_verified=False).delete()  # Clear any old
            OTP.objects.create(user=user, otp_secret=otp_secret)

            #  Send the OTP via email
            subject = "Your OTP Code for Verification"
            message = f"Hi {user.first_name},\n\nYour OTP code is {otp_code}. It is valid for 10 minutes."
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                return Response(
                    {"error": f"Failed to send email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {
                    "data": serializer.data,
                    "message": f"Hi {user.first_name}, your account was created. An OTP has been sent to your email for verification.",
                },
                status=status.HTTP_201_CREATED,
            )


# View for Verifying OTP
class VerifyOTPView(GenericAPIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp_code = serializer.validated_data["otp"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

            try:
                otp = OTP.objects.filter(user=user, is_verified=False)

            except OTP.DoesNotExist:
                return Response(
                    {"error": "No valid OTP found"}, status=status.HTTP_400_BAD_REQUEST
                )

            if otp.is_expired():
                return Response(
                    {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Verify OTP and update the user
            totp = pyotp.TOTP(otp.otp_secret, interval=600)
            if totp.verify(otp_code):
                otp.is_verified = True
                otp.save()
                user.is_verified = True
                user.save()
                return Response(
                    {"message": "OTP verified successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
