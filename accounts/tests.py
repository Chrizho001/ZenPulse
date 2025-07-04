from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, OTP, PasswordResetToken

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Chris",
            last_name="Friday",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertEqual(self.user.get_full_name, "Chris Friday")
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_verified)

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "test@example.com")

    def test_user_tokens(self):
        tokens = self.user.tokens()
        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)


class OTPModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="otpuser@example.com",
            password="otp123",
            first_name="Otp",
            last_name="User"
        )
        self.otp = OTP.objects.create(
            user=self.user,
            otp_secret="SECRET123"
        )

    def test_otp_creation(self):
        self.assertEqual(self.otp.user, self.user)
        self.assertFalse(self.otp.is_verified)
        self.assertIsNotNone(self.otp.expires_at)
        self.assertEqual(str(self.otp), f"{self.user.email} - OTP expires at {self.otp.expires_at}")

    def test_otp_expiry_check(self):
        self.otp.expires_at = timezone.now() - timedelta(minutes=1)
        self.otp.save()
        self.assertTrue(self.otp.is_expired())


class PasswordResetTokenTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="resetuser@example.com",
            password="reset123",
            first_name="Reset",
            last_name="User"
        )
        self.token = PasswordResetToken.objects.create(
            user=self.user,
            otp_secret="RESET123"
        )

    def test_password_reset_token_creation(self):
        self.assertEqual(self.token.user, self.user)
        self.assertFalse(self.token.is_verified)
        self.assertIsNotNone(self.token.expires_at)
        self.assertEqual(str(self.token), f"{self.user.email} - OTP expires at {self.token.expires_at}")

    def test_password_reset_token_expiry_check(self):
        self.token.expires_at = timezone.now() - timedelta(minutes=1)
        self.token.save()
        self.assertTrue(self.token.is_expired())
