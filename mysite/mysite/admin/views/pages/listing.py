from wagtail.admin.views.pages import index as pages_index

from note.models import NoteUserPagePermissionsProxy


def index(request, parent_page_id=None):
    user_perms = NoteUserPagePermissionsProxy(request.user)
    templateResponse = pages_index(request, parent_page_id)
    templateResponse.context_data['user_page_permissions'] = user_perms
    return templateResponse
