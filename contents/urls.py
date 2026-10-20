from django.contrib import admin
from django.urls import path

from contents.api.ninja_api import api
from contents.api.views import redirect_to_docs, root

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", root, name="root"),
    path("docs/", redirect_to_docs, name="docs-redirect"),
    path("api/", api.urls),
]
