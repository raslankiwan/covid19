from django.core.management.base import BaseCommand

from covid19.utils import fill_all_countries


class Command(BaseCommand):
    help = "Fill today stats"

    def handle(self, *args, **options):
        fill_all_countries()
