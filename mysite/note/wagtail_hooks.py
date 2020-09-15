from wagtail.core import hooks


def is_root_page(page):
    return page.depth == 1


@hooks.register('construct_explorer_page_queryset')
def my_hook(parent_page, pages, request):
    if is_root_page(parent_page):
        return pages

    if request.user.is_superuser:
        return pages

    pages = pages.filter(owner=request.user.pk)
    return pages


@hooks.register('construct_main_menu')
def hide_explorer_menu_item_from_frank(request, menu_items):
    if request.user.username == 'user1':
        menu_items[:] = [i for i in menu_items if i.name != 'reports']


@hooks.register('register_page_listing_more_buttons')
def my_page_listing_more_buttons(page, page_perms, is_parent=False, next_url=None):
    print(f'{page_perms=}')
    return []
