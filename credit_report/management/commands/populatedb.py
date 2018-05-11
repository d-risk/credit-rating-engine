from django.core.management.base import BaseCommand

from credit_report.management.commands.parsers import parse
from credit_report.management.commands.randomize import random_companies
from credit_report.management.commands.singtel import create_singtel_company

RANDOMIZE = 'randomize'
SINGTEL = 'singtel'
IMPORT = 'import'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(f'--{RANDOMIZE}', type=int, )
        parser.add_argument(f'--{SINGTEL}', action='store_true', )
        parser.add_argument(f'--{IMPORT}', type=str, )

    def handle(self, *args, **options):
        randomize_companies = options[RANDOMIZE]
        if randomize_companies:
            random_companies(randomize_companies, 2015, 2018)
        if options[SINGTEL]:
            create_singtel_company()
        import_file_name: str = options[IMPORT]
        if import_file_name:
            parse(import_file_name)
