# your_app_name/management/commands/fetch_api.py
from django.core.management.base import BaseCommand
from users.cron import fetch_api_data

class Command(BaseCommand):
    help = "API dan ma'lumot olish uchun command"

    def handle(self, *args, **options):
        self.stdout.write('API ma\'lumot olish boshlandi...')
        fetch_api_data()
        self.stdout.write(self.style.SUCCESS('API ma\'lumot olish tugadi!'))