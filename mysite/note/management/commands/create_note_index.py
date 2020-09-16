from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, no_translations

from note.models import Page
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
        if q.exists():
            self.stdout.write(f'exists: {repr(q.get())}')
            return
    
        User = get_user_model()
        owner = User.objects.filter(is_superuser=True).first()
        note_index = NoteIndexPage(title=options['title'], owner=owner)
        root_page = Page.objects.get(title='Root')
        root_page.add_child(instance=note_index)

        self.stdout.write(self.style.SUCCESS(f'created: {repr(note_index)}'))
