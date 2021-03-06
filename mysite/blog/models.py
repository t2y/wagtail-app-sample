from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.search import index

from wagtailmarkdown.fields import MarkdownField


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = MarkdownField()
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
    ]

    # Export fields over the API
    api_fields = [
        APIField('intro'),
        APIField('body'),
    ]
