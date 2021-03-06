from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.http import Http404
from django.http.request import QueryDict
from django.template.response import TemplateResponse
from django.views.decorators.vary import vary_on_headers

from wagtail.admin.auth import user_has_any_page_permission, user_passes_test
from wagtail.admin.forms.search import SearchForm
from wagtail.search.query import MATCH_ALL
from wagtail.search.utils import parse_query_string

from note.models import NotePage


@vary_on_headers('X-Requested-With')
@user_passes_test(user_has_any_page_permission)
def search(request):
    pages = all_pages = NotePage.objects.all().prefetch_related('content_type').specific()
    if not request.user.is_superuser:
        # filter pages with owner
        pages = all_pages = pages.filter(owner=request.user.pk)

    # filter pages with content type only if Page.objects.all() is used
    # note_page = ContentType.objects.get_for_model(NotePage)
    # pages = all_pages = pages.filter(content_type_id=note_page.pk)

    q = MATCH_ALL
    content_types = []
    pagination_query_params = QueryDict({}, mutable=True)
    ordering = None

    if 'ordering' in request.GET:
        if request.GET['ordering'] in ['title', '-title', 'latest_revision_created_at', '-latest_revision_created_at', 'live', '-live']:
            ordering = request.GET['ordering']

            if ordering == 'title':
                pages = pages.order_by('title')
            elif ordering == '-title':
                pages = pages.order_by('-title')

            if ordering == 'latest_revision_created_at':
                pages = pages.order_by('latest_revision_created_at')
            elif ordering == '-latest_revision_created_at':
                pages = pages.order_by('-latest_revision_created_at')

            if ordering == 'live':
                pages = pages.order_by('live')
            elif ordering == '-live':
                pages = pages.order_by('-live')

    if 'content_type' in request.GET:
        pagination_query_params['content_type'] = request.GET['content_type']

        app_label, model_name = request.GET['content_type'].split('.')

        try:
            selected_content_type = ContentType.objects.get_by_natural_key(app_label, model_name)
        except ContentType.DoesNotExist:
            raise Http404

        pages = pages.filter(content_type=selected_content_type)
    else:
        selected_content_type = None

    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            pagination_query_params['q'] = q

            # Parse query
            filters, query = parse_query_string(q, operator='and', zero_terms=MATCH_ALL)

            # Live filter
            live_filter = filters.get('live') or filters.get('published')
            live_filter = live_filter and live_filter.lower()
            if live_filter in ['yes', 'true']:
                all_pages = all_pages.filter(live=True)
                pages = pages.filter(live=True)
            elif live_filter in ['no', 'false']:
                all_pages = all_pages.filter(live=False)
                pages = pages.filter(live=False)

            # Search
            all_pages = all_pages.custom_search(query, order_by_relevance=not ordering)
            pages = pages.custom_search(query, order_by_relevance=not ordering)

            # Facets
            if pages.supports_facet:
                content_types = [
                    (ContentType.objects.get(id=content_type_id), count)
                    for content_type_id, count in all_pages.facet('content_type_id').items()
                ]

    else:
        form = SearchForm()

    paginator = Paginator(pages, per_page=20)
    pages = paginator.get_page(request.GET.get('p'))

    if request.is_ajax():
        return TemplateResponse(request, "wagtailadmin/pages/search_results.html", {
            'pages': pages,
            'all_pages': all_pages,
            'query_string': q,
            'content_types': content_types,
            'selected_content_type': selected_content_type,
            'ordering': ordering,
            'pagination_query_params': pagination_query_params.urlencode(),
        })
    else:
        return TemplateResponse(request, "wagtailadmin/pages/search.html", {
            'search_form': form,
            'pages': pages,
            'all_pages': all_pages,
            'query_string': q,
            'content_types': content_types,
            'selected_content_type': selected_content_type,
            'ordering': ordering,
            'pagination_query_params': pagination_query_params.urlencode(),
        })
