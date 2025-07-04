from django.core.mail import send_mail
from django.conf import settings


def send_booking_confirmation_email(user, session):
    subject = "Gym Session Booking Confirmation"
    message = f"""
Hi {user.get_full_name},

Your booking has been confirmed!

📅 Date: {session.start_date.date()}
⏰ Time: {session.start_time.strftime('%I:%M %p')}
📝 Description: {session.description}

Thank you for booking with us!
Stay fit 💪🏽
    """.strip()

    send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False
    )
