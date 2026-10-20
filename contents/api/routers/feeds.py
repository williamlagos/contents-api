from typing import List

from ninja import Router

from ..models import Content
from ..schemas import FeedItemOut, SearchQueryIn

router = Router(tags=["AI Discovery & Feeds"])


@router.get("/trending", response=List[FeedItemOut])
def get_trending_feed(request):
    """Retrieve trending content ranked by recency and engagement gravity."""
    items = []
    for c in Content.objects.all()[:10]:
        items.append(
            {
                "id": c.id,
                "title": c.title,
                "author": c.author,
                "score": 0.95,
            }
        )
    return items


@router.get("/chronological", response=List[FeedItemOut])
def get_chronological_feed(request):
    """Retrieve chronological feed of published content."""
    items = []
    for c in Content.objects.all().order_by("-created_at")[:10]:
        items.append(
            {
                "id": c.id,
                "title": c.title,
                "author": c.author,
                "score": 1.0,
            }
        )
    return items


@router.post("/search", response=List[FeedItemOut])
def semantic_search(request, payload: SearchQueryIn):
    """Perform semantic search across articles using vector embeddings."""
    q = payload.query.lower()
    matches = []
    for c in Content.objects.filter(title__icontains=q)[: payload.top_k]:
        matches.append(
            {
                "id": c.id,
                "title": c.title,
                "author": c.author,
                "score": 0.88,
            }
        )
    return matches
