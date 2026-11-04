from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def root(request):
    """Root health check view."""
    return JsonResponse(
        {
            "health": "OK",
            "service": "contents-api",
            "version": "1.0.0",
            "docs": "/api/docs",
        }
    )


def redirect_to_docs(request):
    """Convenience redirect from /docs to /api/docs."""
    return redirect("/api/docs")
