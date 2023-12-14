from django.core.management.base import BaseCommand, CommandError
from tasks.models import User

class Command(BaseCommand):
    """Build automation command to unseed the database."""
    
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        """Unseed the database."""

        User.objects.filter(is_staff=False).delete()

        if User.objects.filter(username="@johndoe").exists():
            User.objects.get(username="@johndoe").delete()

        if User.objects.filter(username="@janedoe").exists():
            User.objects.get(username="@janedoe").delete()