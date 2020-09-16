from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, no_translations

from note.models import NoteIndexPage
from note.models import NotePage


class Command(BaseCommand):
    help = 'Create note page'

    def add_arguments(self, parser):
        parser.add_argument(
            '--index-id', action='store', required=True,
            help='set index page id')
        parser.add_argument(
            '--title', action='store', required=True,
            help='set title')
        parser.add_argument(
            '--intro', action='store', required=True,
            help='set intro')
        parser.add_argument(
            '--owner', action='store', required=True,
            help='set owner')

    @no_translations
    def handle(self, *args, **options):
        index = NoteIndexPage.objects.get(id=options['index_id'])

        User = get_user_model()
        owner = User.objects.get(username=options['owner'])
        note = NotePage(
            title=options['title'],
            intro=options['intro'],
            date=datetime.now(),
            owner=owner)
        index.add_child(instance=note)

        self.stdout.write(self.style.SUCCESS(f'created: {repr(note)}'))
