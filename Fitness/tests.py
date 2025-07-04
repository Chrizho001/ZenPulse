from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from Fitness.models import FitnessBlog, Session
import uuid

User = get_user_model()

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )

    def test_fitness_blog_creation(self):
        blog = FitnessBlog.objects.create(
            title="Benefits of Yoga",
            slug="benefits-of-yoga",
            content="Yoga improves flexibility and mental clarity.",
            author=self.user,
            status="PB"
        )
        self.assertEqual(str(blog), "Benefits of Yoga")
        self.assertEqual(blog.status, "PB")
        self.assertEqual(blog.author, self.user)

    def test_session_creation(self):
        session = Session.objects.create(
            user=self.user,
            start_date=timezone.now(),
            start_time=timezone.now().time(),
            description="Morning yoga session"
        )
        self.assertEqual(str(session), f"Booking {session.id} for {self.user}")
        self.assertEqual(session.user.email, "test@example.com")
