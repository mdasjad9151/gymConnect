# management/commands/delete_expired_requests.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from .models import TrainerRequest

class Command(BaseCommand):
    help = "Deletes TrainerRequests older than 2 days"

    def handle(self, *args, **options):
        expiration_date = timezone.now() - timedelta(minutes=1)
        expired_requests = TrainerRequest.objects.filter(request_date__lt=expiration_date)
        count, _ = expired_requests.delete()
        self.stdout.write(f"Deleted {count} expired requests.")
