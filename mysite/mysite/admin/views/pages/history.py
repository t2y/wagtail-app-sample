from django.http import Http404
from wagtail.admin.views.pages import PageHistoryView

from note.models import is_page_owner


class PageHistoryView(PageHistoryView):

    def get_context_data(self, *args, object_list=None, **kwargs):
        if is_page_owner(self.page, self.request.user):
            return super().get_context_data(*args, object_list=object_list, **kwargs)
        raise Http404('No history view %s can view.' % self.request.user)
