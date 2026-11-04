from .cms import router as cms_router
from .contents import router as contents_router
from .feeds import router as feeds_router
from .shop import router as shop_router
from .social import router as social_router

__all__ = [
    "contents_router",
    "cms_router",
    "social_router",
    "shop_router",
    "feeds_router",
]
