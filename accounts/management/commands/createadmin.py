import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates a default superuser if one doesn't exist"

    def handle(self, *args, **kwargs):
        if os.environ.get("CREATE_SUPERUSER", "false").lower() == "true":
            User = get_user_model()
            email = "chrisfriday033@gmail.com"
            if not User.objects.filter(email=email).exists():
                User.objects.create_superuser(
                    email=email,
                    password="christopher",
                    first_name="Chris",
                    last_name="Friday",
                )
                self.stdout.write(self.style.SUCCESS("Superuser created."))
            else:
                self.stdout.write("Superuser already exists.")
