from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    """
    A Django management command to create test users for development.
    
    Usage: python manage.py create_test_users
    """
    help = 'Creates 5 test users (test1 to test5) for development purposes.'

    def handle(self, *args, **options):
        User = get_user_model()
        
        for i in range(1, 6):
            username = f'test{i}'
            email = f'test{i}@example.com'
            password = 'password123'

            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'User "{username}" already exists. Skipping.'))
                continue

            User.objects.create_user(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created user "{username}" with email "{email}".'))

        self.stdout.write(self.style.SUCCESS('Finished creating test users.'))
