from django.core.management.base import BaseCommand

from covid19.clients.covid19_client import Covid19Client


class Command(BaseCommand):
    help = "Fill today stats"

    def handle(self, *args, **options):
        Covid19Client().fill_today_for_all()
