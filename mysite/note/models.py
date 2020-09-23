from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.models import PageManager
from wagtail.core.models import PagePermissionTester
from wagtail.core.models import BasePageManager
from wagtail.core.models import PageQuerySet
from wagtail.core.models import UserPagePermissionsProxy
from wagtail.search import index
from wagtail.search.queryset import SearchableQuerySetMixin


def is_page_owner(page, user):
    if not user.is_active:
        return False
    if user.is_superuser:
        return True
    if page.owner is None:
        return True
    return page.owner.pk == user.pk


class NotePagePermissionTester(PagePermissionTester):

    def can_edit(self):
        print('called can_edit')
        return is_page_owner(self.page, self.user)

    def can_delete(self, ignore_bulk=False):
        print('called can_delete')
        return is_page_owner(self.page, self.user)

    def can_unpublish(self):
        print('called can_unpublish')
        return is_page_owner(self.page, self.user)

    def can_publish(self):
        print('called can_publish')
        return is_page_owner(self.page, self.user)

    def can_lock(self):
        print('called can_lock')
        return is_page_owner(self.page, self.user)

    def can_unlock(self):
        print('called can_unlock')
        return is_page_owner(self.page, self.user)

    def can_move(self):
        print('called can_move')
        return is_page_owner(self.page, self.user)

    def can_copy(self):
        print('called can_copy')
        return is_page_owner(self.page, self.user)

    def can_move_to(self, destination):
        print(f'called can_move_to: {destination=}')
        return False

    def can_copy_to(self, destination, recursive=False):
        print(f'called can_copy_to: {destination=}, {recursive=}')
        return False

    def can_view_revisions(self):
        print('called can_view_revisions')
        return is_page_owner(self.page, self.user)


class NoteUserPagePermissionsProxy(UserPagePermissionsProxy):

    def for_page(self, page):
        return NotePagePermissionTester(self, page)


class NotePageQuerySet(PageQuerySet):

    def custom_search(self, query, fields=None, operator=None,
                      order_by_relevance=True, partial_match=True,
                      backend='default'):
        print(f'called custom_search: {query}')
        return self.search(query, fields, operator, order_by_relevance,
                partial_match, backend)


NotePageManager = PageManager.from_queryset(NotePageQuerySet)


class AbstractNotePage(Page):

    objects = NotePageManager()

    class Meta:
        abstract = True

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.title} ({self.id})>'

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

    subpage_types = []  # prevent child page
