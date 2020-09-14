from wagtail.core import hooks


def is_root_page(page):
    return page.depth == 1


@hooks.register('construct_explorer_page_queryset')
def my_hook(parent_page, pages, request):
    if is_root_page(parent_page):
        return pages

    filtered = []
    for page in pages:
        if page.owner.id == request.user.id:
            filtered.append(page)
    print(filtered)
    return filtered


@hooks.register('construct_main_menu')
def hide_explorer_menu_item_from_frank(request, menu_items):
    if request.user.username == 'user1':
        menu_items[:] = [i for i in menu_items if i.name != 'reports']
