"""Root URL configuration.

Note the ordering: everything that is not `admin/` or `api/` falls through to
the shortener, whose `<slug:slug>/` pattern matches any single path segment.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    # Uploaded files (preview images). The app serves them itself, in
    # production too: there are few and they are small, and it saves a web
    # server in front of the app. Must stay before the shortener's catch-all.
    re_path(
        r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip("/"),
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
    path("", include("shortener.urls")),
]
