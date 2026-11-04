from ninja import NinjaAPI

from .routers import (
    cms_router,
    contents_router,
    feeds_router,
    shop_router,
    social_router,
)
from .schemas import HealthOut

api = NinjaAPI(
    title="Contents API",
    version="1.0.0",
    description=(
        "Unified Headless CMS, Plethora publishing, ActivityPub social federation, "
        "and multi-rail e-commerce engine."
    ),
    docs_url="/docs",
)


@api.get("/health", response=HealthOut, tags=["System"])
def api_health(request):
    """System health check endpoint."""
    return {
        "health": "OK",
        "status": "operational",
        "service": "contents-api",
        "version": "1.0.0",
        "framework": "django-ninja",
    }


# Mount all modular routers
api.add_router("/contents", contents_router)
api.add_router("/cms", cms_router)
api.add_router("/social", social_router)
api.add_router("/shop", shop_router)
api.add_router("/feeds", feeds_router)
