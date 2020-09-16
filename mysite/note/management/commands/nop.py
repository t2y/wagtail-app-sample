from django.core.management.base import BaseCommand, no_translations


class Command(BaseCommand):
    help = 'No operation command'

    def add_arguments(self, parser):
        parser.set_defaults(
            verbose=False,
        )
        parser.add_argument(
            '--verbose', action='store_true', help='set verbose mode')

    @no_translations
    def handle(self, *args, **options):
        if options['verbose']:
            self.stdout.write(self.style.NOTICE('verbose option is specified'))
        self.stdout.write(self.style.SUCCESS('Successfully run'))
