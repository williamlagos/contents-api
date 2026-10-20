from django.urls import path

from .ninja_api import api
from .views import redirect_to_docs, root

urlpatterns = [
    path("", root, name="api-root"),
    path("docs/", redirect_to_docs, name="api-docs-redirect"),
    path("api/", api.urls),
]
