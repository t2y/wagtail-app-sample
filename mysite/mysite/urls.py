from django.conf import settings
from django.urls import path, re_path
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from .api import api_router
from .admin.views.pages import listing as admin_listing
from .admin.views.pages import history as admin_history


urlpatterns = [
    path('api/v2/', api_router.urls),

    url(r'^django-admin/', admin.site.urls),

    # Override admin pages view
    path('admin/pages/', admin_listing.index, name='wagtailadmin_explore_root'),
    path('admin/pages/<int:parent_page_id>/', admin_listing.index, name='wagtailadmin_explore'),
    path('admin/pages/<int:page_id>/history/', admin_history.PageHistoryView.as_view(), name='history'),
    url(r'^admin/', include(wagtailadmin_urls)),

    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    # Ensure that the api_router line appears above the default Wagtail page serving route
    re_path(r'^', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r"^pages/", include(wagtail_urls)),
]
