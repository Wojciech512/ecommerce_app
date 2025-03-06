from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Tworzy superusera, jeśli jeszcze nie istnieje."

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = "userAdmin"
        password = "Test123!"
        email = "admin@example.com"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' został utworzony."))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' już istnieje."))
