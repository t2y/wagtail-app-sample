from wagtail.admin.views.pages import listing

from note.models import NoteUserPagePermissionsProxy


def index(request, parent_page_id=None):
    user_perms = NoteUserPagePermissionsProxy(request.user)
    templateResponse = listing.index(request, parent_page_id)
    templateResponse.context_data['user_page_permissions'] = user_perms
    return templateResponse
