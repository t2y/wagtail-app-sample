from django.core.management.base import BaseCommand, no_translations

from note.models import NoteIndexPage


class Command(BaseCommand):
    help = 'Create note index'

    def add_arguments(self, parser):
        parser.set_defaults(
            title=None,
        )
        parser.add_argument(
            '--title', action='store', required=True,
            help='set title')

    @no_translations
    def handle(self, *args, **options):
        q = NoteIndexPage.objects.filter(title=options['title'])
        if not q.exists():
            self.stdout.write(f"does not exist: {options['title']}")
            return

        note_index = q.get()
        self.stdout.write(f'{repr(note_index)}')
        for child in note_index.get_children():
            self.stdout.write(f' - {repr(child)}')
        note_index.delete()

        self.stdout.write(self.style.SUCCESS(f'deleted: {repr(note_index)}'))
