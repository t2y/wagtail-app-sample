from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import GroupPagePermission
from wagtail.core.models import Page
from wagtail.core.models import UserPagePermissionsProxy
from wagtail.search import index


class NotePagePermissionTester:

    def __init__(self, user_perms, page):
        self.user = user_perms.user
        self.user_perms = user_perms
        self.page = page
        self.page_is_root = page.depth == 1  # Equivalent to page.is_root()

        if self.user.is_active and not self.user.is_superuser:
            self.permissions = set(
                perm.permission_type for perm in user_perms.permissions
                if self.page.path.startswith(perm.page.path)
            )

    def user_has_lock(self):
        return self.page.locked_by_id == self.user.pk

    def page_locked(self):
        return False

    def can_publish(self):
        return True

    def can_edit(self):
        print('called can_edit')
        return self.user.id == self.page.owner.id

    def can_delete(self, ignore_bulk=False):
        print('called can_delete')
        return False

    def can_add_subpage(self):
        print('called can_add_subpage')
        return False

    def can_move_to(self, destination):
        print(f'called can_move_to: {destination}')
        return False


class NoteUserPagePermissionsProxy(UserPagePermissionsProxy):

    def __init__(self, user):
        self.user = user
        if user.is_active and not user.is_superuser:
            self.permissions = []

    def for_page(self, page):
        return NotePagePermissionTester(self, page)


class AbstractNotePage(Page):

    class Meta:
        abstract = True

    def get_admin_display_title(self):
        title = super().get_admin_display_title()
        return title + f' (owner: {self.owner})'

    def permissions_for_user(self, user):
        user_perms = NoteUserPagePermissionsProxy(user)
        return user_perms.for_page(self)


class NoteIndexPage(AbstractNotePage):

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class NotePage(AbstractNotePage):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
    ]
